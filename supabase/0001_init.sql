-- OPSIS — schéma initial (Supabase / PostgreSQL)
-- À exécuter une fois : Supabase > SQL Editor > coller > Run.

-- ============ CONTENU ============
create table if not exists public.stories (
  id           text primary key,                -- ex. « ar01 »
  series       text not null,                   -- code de série : ar, cs, fa…
  pos          int  not null,                   -- ordre dans la série
  status       text not null default 'live' check (status in ('live','archived')),
  data         jsonb not null,                  -- {id,name,sub,dates,country,body[],src…}
  lens         jsonb,                           -- versions 3 / 5 / 10 minutes
  cover        text,                            -- couverture SVG (facultatif)
  published_at timestamptz not null default now(),
  updated_at   timestamptz not null default now(),
  sync_at      timestamptz generated always as (greatest(updated_at, published_at)) stored
);
create index if not exists stories_sync_idx on public.stories (sync_at);
create index if not exists stories_series_idx on public.stories (series, pos);

create table if not exists public.content_meta (
  key        text primary key,                  -- BOOK, BSRC, SCHEDULE…
  value      jsonb not null,
  updated_at timestamptz not null default now()
);

create or replace function public.touch_updated_at() returns trigger language plpgsql as $$
begin new.updated_at := now(); return new; end $$;
drop trigger if exists stories_touch on public.stories;
create trigger stories_touch before update on public.stories for each row execute function public.touch_updated_at();
drop trigger if exists meta_touch on public.content_meta;
create trigger meta_touch before update on public.content_meta for each row execute function public.touch_updated_at();

alter table public.stories enable row level security;
alter table public.content_meta enable row level security;
-- lecture publique, mais seulement ce qui est déjà publié : une histoire datée dans le futur reste invisible
drop policy if exists stories_read on public.stories;
create policy stories_read on public.stories for select to anon, authenticated using (published_at <= now());
drop policy if exists meta_read on public.content_meta;
create policy meta_read on public.content_meta for select to anon, authenticated using (true);
-- aucune écriture côté application : seul le service (clé service_role) peut publier

-- ============ COMPTES : ÉTAT DE L'UTILISATEUR ============
create table if not exists public.user_state (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  ledger     jsonb not null default '{}'::jsonb,   -- { "read.pt01": {"v":true,"t":1767500000000}, … }
  updated_at timestamptz not null default now()
);
alter table public.user_state enable row level security;
drop policy if exists state_own on public.user_state;
create policy state_own on public.user_state for all to authenticated
  using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- fusion atomique : pour chaque clé, la valeur la plus récente gagne (deux appareils ne s'écrasent jamais)
create or replace function public.merge_user_state(p jsonb) returns jsonb
language plpgsql security invoker set search_path = public as $$
declare
  uid uuid := auth.uid(); cur jsonb; res jsonb; k text; v jsonb;
begin
  if uid is null then raise exception 'not authenticated' using errcode = '28000'; end if;
  insert into user_state (user_id) values (uid) on conflict (user_id) do nothing;
  select ledger into cur from user_state where user_id = uid for update;
  res := coalesce(cur, '{}'::jsonb);
  for k, v in select * from jsonb_each(coalesce(p, '{}'::jsonb)) loop
    if jsonb_typeof(v) = 'object' and (v->>'t') ~ '^[0-9]+$'
       and (not jsonb_exists(res, k) or (res->k->>'t')::numeric < (v->>'t')::numeric) then
      res := jsonb_set(res, array[k], v, true);
    end if;
  end loop;
  if length(res::text) > 2000000 then raise exception 'state too large'; end if;
  update user_state set ledger = res, updated_at = now() where user_id = uid;
  return res;
end $$;
revoke all on function public.merge_user_state(jsonb) from public, anon;
grant execute on function public.merge_user_state(jsonb) to authenticated;

-- suppression du compte (obligatoire pour l'App Store) : efface l'utilisateur, l'état part en cascade
create or replace function public.delete_my_account() returns void
language plpgsql security definer set search_path = public, auth as $$
begin
  if auth.uid() is null then raise exception 'not authenticated' using errcode = '28000'; end if;
  delete from auth.users where id = auth.uid();
end $$;
revoke all on function public.delete_my_account() from public, anon;
grant execute on function public.delete_my_account() to authenticated;
