/* Couvertures de la série « Jusqu'à la chute » : portraits graphiques reconnaissables (signes distinctifs), générés en SVG */
const fs=require('fs'),path=require('path');
const root=path.join(__dirname,'..');
const covers=JSON.parse(fs.readFileSync(path.join(root,'data/covers.json'),'utf8'));
const SK={L:'#F3D2B0',M:'#DDAE7C',T:'#B8814F',D:'#7E4D34'};
const HC={k:'#16110F',br:'#53341F',bl:'#E6C56B',gr:'#B8B5AE',w:'#EEEBE4',rd:'#B5482A'};
const K='#0C0A0B',C='#F4E6C8';
function shade(h,f){const n=parseInt(h.slice(1),16);let r=n>>16,g=(n>>8)&255,b=n&255;r=Math.round(r*f);g=Math.round(g*f);b=Math.round(b*f);return '#'+[r,g,b].map(x=>x.toString(16).padStart(2,'0')).join('');}
/* spec : [id, sexe, peau, cheveux, couleurCheveux, barbe, lunettes, chapeau, vêtement, couleurVêtement, accessoires[]] */
const P=[
['pt01','f','L','pigtails','br','','','', 'dress','#3B6EA8',['ribbons','slipper']],
['pt02','m','L','curly','k','','','fedora','suit','#1A1A20',['glove']],
['pt03','f','L','long','bl','','','','tee','#E0457B',['headset']],
['pt04','m','L','short','bl','','','','tee','#C2392B',['cheeks']],
['pt05','f','L','wavy','bl','','','','tee','#6AA9A0',['sparkle']],
['pt06','m','M','curly','k','','','','jersey','#6FA8DC',['n10','ball']],
['pt07','m','D','bald','k','','','','tee','#14121A',['boxing','tattoo']],
['pt08','m','L','bald','k','goatee','','bandana','jersey','#E8D44D',['bike','earring']],
['pt09','m','M','long','k','','','fbhelmet','jersey','#4A79B8',[]],
['pt10','m','L','short','br','','','','jersey','#2B2F3A',['gkgloves']],
['pt11','f','L','beehive','k','','cat','','dress','#E5E0D2',['wing','earring']],
['pt12','m','L','shag','bl','stubble','heart','','sweater','#7A8F5A',['guitar']],
['pt13','f','D','bighair','k','','','','dress','#E8E2D6',['mic']],
['pt14','m','L','swept','bl','stubble','','headphones','tee','#E8E8EE',[]],
['pt15','f','L','pixie','br','','','','dress','#2A2A33',['pearls']],
['pt16','f','L','pixie','bl','','','tiara','dress','#7BA7D6',['pearls']],
['pt17','f','L','bald','k','','','','tee','#E8E2D6',['earring']],
['pt18','m','D','short','k','','','headband','tee','#E8B93C',['chain']],
['pt19','m','L','short','br','stubble','round','trilby','tee','#2D2D38',['cube']],
['pt20','m','M','quiff','k','must','','','ruffle','#6B3FA0',['lovesym']],
['pt21','m','L','short','gr','','round','cowboy','shirt','#8B5A2B',['check']],
['pt22','m','D','afro','k','','sun','','jacket','#C9A227',[]],
['pt23','m','L','messy','bl','stubble','','','tee','#2A2A30',['smirk']],
['pt24','m','L','swept','gr','stubble','','','jacket','#222228',['knife','cig']],
['pt25','m','D','locs','k','','','crown3','tee','#E8E2D6',['paint']],
['pt26','m','L','short','br','','','','suit','#16141A',['skull']],
['pt27','m','L','slick','k','','big','','tux','#16141A',['bowtie']],
['pt28','m','L','short','gr','','','spacehelmet','suit','#E8E8EE',['flag']],
['pt29','m','L','bald','k','','','swimcap','tee','#16141A',['goggles','medals']],
['pt30','m','L','long','bl','stubble','','headband','tee','#E8E8EE',['racket']],
['pt31','m','M','mullet','bl','','','capback','tee','#E5543C',['racket']],
['pt32','f','L','ponytail','bl','','','','tee','#16141A',['boxing']],
['pt33','f','L','bun','bl','','','','turtle','#101014',['vial','lips']],
['pt34','m','L','curly','br','','','','tee','#7FA8C8',['coin']],
['pt35','m','M','long','k','beard','','','shirt','#1E2A44',[]],
['pt36','f','L','bob','bl','','','','dress','#E8E2D6',['pearls']],
['pt37','m','T','short','k','','','','hoodie','#6B6B76',['shoe']],
['pt38','m','L','bald','k','','','','suit','#1A1A22',['tie','bars']],
['pt39','m','L','short','br','stubble','','','tee','#3A3A46',['padlock']],
['pt40','m','M','short','gr','','round','','suit','#1A1A22',['case']],
['pt41','m','L','short','w','','round','','suit','#1A1A22',['pyramid']],
['pt42','m','L','slick','br','','','','suit','#16141A',['cash']],
['pt43','m','L','bald','k','','sun','cyclehelmet','jersey','#F2D23C',['wristband']],
['pt44','m','D','short','k','','','','suit','#1A1A22',['glove']],
['pt45','m','L','balding','gr','beard','round','','robe','#E8E2D6',['bars']],
['pt46','m','L','short','br','stubble','','','tee','#2B2F3A',['blades']],
['pt47','m','T','short','k','','','cap','polo','#C62828',['club']],
['pt48','m','L','swept','br','goatee','tint','','jacket','#2A2A30',[]],
['pt49','m','D','short','k','must','','','shirt','#6B3F2A',['mic','brick']],
['pt50','m','T','short','k','','','','shirt','#C9A06A',['bowtie']],
['pt51','f','D','ponytail','k','','','','dress','#2A6FB0',['medals','star']],
['pt52','m','L','buzz','bl','stubble','','hood','hoodie','#16141A',['mic']],
];
function figure(sp,acc,mid){
  const [id,g,skn,hair,hcol,beard,gl,hat,cloth,ccol,props]=sp;
  const sk=SK[skn],skd=shade(sk,.78),hc=HC[hcol]||HC.k,fem=g==='f';
  const rx=fem?27:30,ry=fem?36:38;
  let s='';
  const has=k=>props.includes(k);
  /* arrière-plan de la figure */
  if(has('lovesym'))s+=`<g fill="none" stroke="${acc}" stroke-width="7" opacity=".9"><circle cx="100" cy="108" r="58"/><path d="M100 166 V232 M72 206 H128"/><path d="M146 66 L172 40 M172 40 H150 M172 40 V62"/></g>`;
  if(has('cube'))s+=`<g opacity=".95"><path d="M150 42 L178 54 L150 66 L122 54Z" fill="${C}"/><path d="M122 54 L150 66 V98 L122 86Z" fill="#7BAE5A"/><path d="M150 66 L178 54 V86 L150 98Z" fill="#5B8A3E"/></g>`;
  if(has('brick'))s+=`<g stroke="${shade(acc,.5)}" stroke-width="2" opacity=".5" fill="none"><path d="M0 80H200M0 130H200M0 180H200M0 230H200M40 80V130M120 80V130M80 130V180M160 130V180M40 180V230M120 180V230"/></g>`;
  if(has('pyramid'))s+=`<path d="M100 14 L160 100 H40Z" fill="none" stroke="${acc}" stroke-width="3" opacity=".7"/>`;
  if(has('bars'))s+=`<g fill="${shade(acc,.55)}" opacity=".7">${[30,56,82,118,144,170].map(x=>`<rect x="${x}" y="20" width="6" height="190"/>`).join('')}</g>`;
  if(has('padlock'))s+=`<g transform="translate(138 36)"><path d="M6 14 V8 a10 10 0 0 1 20 0 V14" fill="none" stroke="${C}" stroke-width="5"/><rect x="0" y="14" width="32" height="26" rx="5" fill="${acc}"/></g>`;
  if(hat==='hood')s+=`<path d="M46 214 Q36 56 100 40 Q164 56 154 214 L130 160 Q138 96 100 86 Q62 96 70 160Z" fill="${ccol}" stroke="${shade(ccol,2.2)}" stroke-width="2"/>`;
  if(hair==='afro')s+=`<circle cx="100" cy="86" r="58" fill="${hc}"/>`;
  if(hair==='bighair')s+=`<circle cx="100" cy="88" r="54" fill="${hc}"/><circle cx="62" cy="116" r="22" fill="${hc}"/><circle cx="138" cy="116" r="22" fill="${hc}"/>`;
  if(hair==='long')s+=`<path d="M64 108 Q60 60 100 58 Q140 60 136 108 L148 200 Q122 196 118 150 L82 150 Q78 196 52 200Z" fill="${hc}"/>`;
  if(hair==='wavy')s+=`<path d="M64 108 Q58 58 100 56 Q142 58 136 108 Q150 150 140 178 Q132 160 122 170 Q118 150 118 140 L82 140 Q82 150 78 170 Q68 160 60 178 Q50 150 64 108Z" fill="${hc}"/>`;
  if(hair==='beehive')s+=`<ellipse cx="100" cy="46" rx="30" ry="44" fill="${hc}"/><path d="M70 100 Q66 60 100 56 Q134 60 130 100 L136 130 Q120 110 100 108 Q80 110 64 130Z" fill="${hc}"/>`;
  if(hair==='curly'||hair==='shag'){[[66,92,17],[80,72,19],[102,64,19],[124,72,19],[136,92,17],[64,116,13],[136,116,13],[68,138,11],[132,138,11]].forEach(([x,y,r])=>s+=`<circle cx="${x}" cy="${y}" r="${r}" fill="${hc}"/>`);}
  if(hair==='bob')s+=`<path d="M66 118 Q60 58 100 56 Q140 58 134 118 L134 150 Q118 146 114 132 L86 132 Q82 146 66 150Z" fill="${hc}"/>`;
  if(hair==='ponytail'||hair==='bun'){ if(hair==='ponytail')s+=`<path d="M124 78 Q172 80 160 150 Q156 112 122 100Z" fill="${hc}"/>`; else s+=`<circle cx="100" cy="52" r="18" fill="${hc}"/>`;}
  if(hair==='pigtails')s+=`<path d="M70 100 Q44 110 48 170 Q64 150 74 118Z" fill="${hc}"/><path d="M130 100 Q156 110 152 170 Q136 150 126 118Z" fill="${hc}"/>`;
  if(hair==='locs')[[78,74,66,26],[90,70,86,18],[100,68,100,14],[110,70,114,18],[122,74,134,26],[68,86,52,44],[132,86,148,44]].forEach(([x1,y1,x2,y2])=>s+=`<path d="M${x1} ${y1} L${x2} ${y2}" stroke="${hc}" stroke-width="9" stroke-linecap="round"/>`);
  if(hair==='mullet')s+=`<path d="M68 112 L58 168 Q80 156 84 128Z" fill="${hc}"/><path d="M132 112 L142 168 Q120 156 116 128Z" fill="${hc}"/>`;
  /* cou + épaules */
  const shw=fem?'M42 300 L46 244 Q50 222 78 212 L90 206 L110 206 L122 212 Q150 222 154 244 L158 300Z':'M26 300 L32 242 Q38 218 70 208 L88 202 L112 202 L130 208 Q162 218 168 242 L174 300Z';
  s+='<g transform="translate(0 -26)">';
  s+=`<rect x="${fem?88:87}" y="138" width="${fem?24:26}" height="74" fill="${skd}"/>`;
  s+=`<path d="${shw}" fill="${ccol}"/>`;
  if(cloth==='suit'||cloth==='tux'||cloth==='jacket')s+=`<path d="M86 204 L100 258 L114 204 L100 214Z" fill="${C}" opacity=".92"/><path d="M86 204 L72 252 M114 204 L128 252" stroke="${shade(ccol,2.4)}" stroke-width="3" fill="none"/>`;
  if(cloth==='turtle')s+=`<rect x="84" y="150" width="32" height="58" rx="10" fill="${ccol}"/>`;
  if(cloth==='ruffle')s+=`<path d="M70 210 Q80 196 90 208 Q100 196 110 208 Q120 196 130 210 L124 236 Q100 226 76 236Z" fill="${C}"/>`;
  if(cloth==='hoodie'||cloth==='polo'||cloth==='shirt')s+=`<path d="M84 204 L100 224 L116 204" fill="none" stroke="${shade(ccol,1.9)}" stroke-width="4"/>`;
  if(cloth==='jersey')s+=`<path d="M84 204 Q100 222 116 204" fill="none" stroke="${C}" stroke-width="4"/>`;
  if(has('n10'))s+=`<text x="100" y="272" text-anchor="middle" font-family="Impact,Arial Black,sans-serif" font-size="46" fill="${C}">10</text>`;
  if(has('pearls'))for(let i=0;i<9;i++){const a=Math.PI*(.12+i*.095);s+=`<circle cx="${100-Math.cos(a)*22+0}" cy="${208+Math.sin(a)*20}" r="3.2" fill="${C}"/>`;}
  if(has('chain'))s+=`<path d="M78 206 Q100 252 122 206" fill="none" stroke="#E8B93C" stroke-width="4"/><circle cx="100" cy="240" r="7" fill="#E8B93C"/>`;
  if(has('medals'))s+=`<path d="M84 202 L96 250 M116 202 L104 250" stroke="${acc}" stroke-width="5"/>${[[88,256],[100,262],[112,256]].map(([x,y])=>`<circle cx="${x}" cy="${y}" r="9" fill="#E8B93C" stroke="#9A7414" stroke-width="2"/>`).join('')}`;
  if(has('wristband'))s+='';
  if(has('skull'))s+=`<g transform="translate(100 248)"><path d="M-14 -6 Q-14 -22 0 -22 Q14 -22 14 -6 Q14 2 8 4 L8 12 H-8 V4 Q-14 2 -14 -6Z" fill="${C}"/><circle cx="-6" cy="-6" r="3.6" fill="${K}"/><circle cx="6" cy="-6" r="3.6" fill="${K}"/></g>`;
  if(has('bowtie'))s+=`<path d="M100 207 L82 198 V216Z M100 207 L118 198 V216Z" fill="${acc}"/><circle cx="100" cy="207" r="4" fill="${shade(acc,.6)}"/>`;
  if(has('tie'))s+=`<path d="M96 206 L104 206 L108 250 L100 262 L92 250Z" fill="${acc}"/>`;
  s+='</g>';
  /* oreilles + visage */
  s+=`<circle cx="${100-rx}" cy="116" r="6.5" fill="${sk}"/><circle cx="${100+rx}" cy="116" r="6.5" fill="${sk}"/>`;
  s+=`<ellipse cx="100" cy="112" rx="${rx}" ry="${ry}" fill="${sk}"/>`;
  /* traits */
  const ey=has('cheeks')?106:108;
  s+=`<ellipse cx="88" cy="${ey}" rx="3.2" ry="2.4" fill="${K}"/><ellipse cx="112" cy="${ey}" rx="3.2" ry="2.4" fill="${K}"/>`;
  s+=`<path d="M82 ${ey-8} Q88 ${ey-11} 94 ${ey-8} M106 ${ey-8} Q112 ${ey-11} 118 ${ey-8}" stroke="${hc}" stroke-width="2.4" fill="none" stroke-linecap="round"/>`;
  s+=`<path d="M100 112 L97 126 Q100 128 103 126" stroke="${shade(sk,.62)}" stroke-width="2" fill="none" stroke-linecap="round"/>`;
  if(has('cheeks'))s+=`<ellipse cx="100" cy="136" rx="7" ry="9" fill="${K}"/>`;
  else if(has('smirk'))s+=`<path d="M88 136 Q104 144 116 130" stroke="${K}" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M116 130 L122 124 M88 136 L82 130" stroke="${acc}" stroke-width="2.4" stroke-linecap="round"/>`;
  else s+=`<path d="M90 136 Q100 142 110 136" stroke="${has('lips')?'#C2182B':shade(sk,.45)}" stroke-width="${has('lips')?4:2.6}" fill="none" stroke-linecap="round"/>`;
  if(has('wing'))s+=`<path d="M78 ${ey+1} L66 ${ey-6} M122 ${ey+1} L134 ${ey-6}" stroke="${K}" stroke-width="3" stroke-linecap="round"/>`;
  if(has('tattoo'))s+=`<path d="M118 ${ey-8} Q128 ${ey} 120 ${ey+12} Q114 ${ey+4} 118 ${ey-8}Z" fill="${K}"/>`;
  if(has('earring'))s+=`<circle cx="${100-rx}" cy="128" r="4" fill="none" stroke="#E8B93C" stroke-width="2.4"/>`;
  /* barbe */
  if(beard==='full'||beard==='beard')s+=`<path d="M70 118 Q72 156 100 162 Q128 156 130 118 Q122 142 100 144 Q78 142 70 118Z" fill="${hc}"/>`;
  if(beard==='stubble')s+=`<path d="M72 122 Q76 152 100 156 Q124 152 128 122 Q120 146 100 148 Q80 146 72 122Z" fill="${hc}" opacity=".55"/>`;
  if(beard==='goatee')s+=`<path d="M92 140 Q100 138 108 140 L106 156 Q100 162 94 156Z" fill="${hc}"/>`;
  if(beard==='must'||has('lovesym')||hair==='quiff')s+=`<path d="M86 130 Q100 124 114 130 Q108 134 100 132 Q92 134 86 130Z" fill="${hc}"/>`;
  /* cheveux devant */
  const top=`M70 106 Q66 66 100 62 Q134 66 130 106 Q124 86 100 84 Q76 86 70 106Z`;
  if(['short','curly'].includes(hair)&&hair==='short')s+=`<path d="${top}" fill="${hc}"/>`;
  if(hair==='buzz')s+=`<path d="M70 102 Q70 72 100 70 Q130 72 130 102 Q122 84 100 83 Q78 84 70 102Z" fill="${hc}"/>`;
  if(hair==='swept')s+=`<path d="M68 104 Q62 62 104 56 Q136 58 132 100 Q124 80 106 80 Q84 80 68 104Z" fill="${hc}"/>`;
  if(hair==='slick')s+=`<path d="M70 104 Q68 66 100 62 Q132 66 130 104 Q120 80 100 78 Q80 80 70 104Z" fill="${hc}"/>`;
  if(hair==='quiff')s+=`<path d="M66 102 Q58 50 106 42 Q136 42 134 76 Q132 92 132 104 Q122 80 100 78 Q78 82 66 102Z" fill="${hc}"/>`;
  if(hair==='pixie')s+=`<path d="M70 112 Q64 62 100 60 Q136 62 130 112 Q128 92 112 84 Q96 96 70 112Z" fill="${hc}"/>`;
  if(hair==='messy')s+=`<path d="M66 110 Q60 58 100 56 Q142 58 134 110 L140 140 L128 118 Q124 86 100 84 Q78 88 72 118 L60 140Z" fill="${hc}"/>`;
  if(hair==='long'||hair==='wavy'||hair==='bob')s+=`<path d="M68 104 Q66 64 100 62 Q134 64 132 104 Q112 84 90 90 Q78 96 68 104Z" fill="${hc}"/>`;
  if(hair==='mullet')s+=`<path d="${top}" fill="${hc}"/>`;
  if(hair==='balding')s+=`<path d="M70 112 Q66 90 74 82 L78 100Z M130 112 Q134 90 126 82 L122 100Z" fill="${hc}"/>`;
  if(hair==='pigtails'||hair==='ponytail'||hair==='bun')s+=`<path d="M70 104 Q66 62 100 60 Q134 62 130 104 Q112 80 70 104Z" fill="${hc}"/>`;
  if(hair==='curly'||hair==='shag')s+=`<path d="M72 104 Q76 82 100 80 Q124 82 128 104 Q112 92 100 94 Q88 92 72 104Z" fill="${hc}"/>`;
  if(hair==='messy'||hair==='bighair'||hair==='afro'||hair==='locs'||hair==='beehive'){}
  if(has('ribbons'))s+=`<path d="M50 130 l-8 -6 v14z M50 130 l8 -6 v14z M150 130 l-8 -6 v14z M150 130 l8 -6 v14z" fill="${acc}"/>`.replace(/M50 130 l-8 -6 v14z M50 130 l8 -6 v14z/,'M52 126 l-8 -7 v15z M52 126 l8 -7 v15z');
  /* lunettes */
  if(gl==='sun')s+=`<rect x="67" y="${ey-8}" width="28" height="17" rx="6" fill="${K}" stroke="${C}" stroke-width="2.4"/><rect x="105" y="${ey-8}" width="28" height="17" rx="6" fill="${K}" stroke="${C}" stroke-width="2.4"/><path d="M95 ${ey-2} H105" stroke="${C}" stroke-width="2.6"/>`;
  if(gl==='tint')s+=`<circle cx="86" cy="${ey}" r="11" fill="#7A4A2A" stroke="#E8B93C" stroke-width="2.2"/><circle cx="114" cy="${ey}" r="11" fill="#7A4A2A" stroke="#E8B93C" stroke-width="2.2"/><path d="M97 ${ey} H103" stroke="#E8B93C" stroke-width="2.2"/>`;
  if(gl==='round')s+=`<circle cx="86" cy="${ey}" r="11" fill="none" stroke="${K}" stroke-width="2.6"/><circle cx="114" cy="${ey}" r="11" fill="none" stroke="${K}" stroke-width="2.6"/><path d="M97 ${ey} H103" stroke="${K}" stroke-width="2.6"/>`;
  if(gl==='big')s+=`<rect x="66" y="${ey-13}" width="31" height="27" rx="3" fill="none" stroke="${K}" stroke-width="4"/><rect x="103" y="${ey-13}" width="31" height="27" rx="3" fill="none" stroke="${K}" stroke-width="4"/><path d="M97 ${ey-4} H103" stroke="${K}" stroke-width="4"/>`;
  if(gl==='cat')s+=`<path d="M66 ${ey+2} Q86 ${ey-14} 96 ${ey+2} Q86 ${ey+8} 66 ${ey+2}Z M104 ${ey+2} Q114 ${ey-14} 134 ${ey+2} Q114 ${ey+8} 104 ${ey+2}Z" fill="none" stroke="${K}" stroke-width="2.6"/>`;
  if(gl==='heart')s+=`${[86,114].map(x=>`<path d="M${x} ${ey+9} L${x-12} ${ey-3} Q${x-14} ${ey-12} ${x-6} ${ey-11} Q${x} ${ey-10} ${x} ${ey-5} Q${x} ${ey-10} ${x+6} ${ey-11} Q${x+14} ${ey-12} ${x+12} ${ey-3}Z" fill="${acc}" stroke="${K}" stroke-width="2"/>`).join('')}`;
  /* chapeaux */
  if(hat==='fedora')s+=`<g transform="rotate(-7 100 78)"><ellipse cx="100" cy="80" rx="56" ry="10" fill="${K}"/><path d="M72 80 Q70 40 100 38 Q130 40 128 80Z" fill="${K}"/><path d="M72 76 H128 V68 H72Z" fill="${acc}"/></g>`;
  if(hat==='trilby')s+=`<g transform="rotate(-4 100 78)"><ellipse cx="100" cy="80" rx="44" ry="7" fill="${K}"/><path d="M74 80 Q72 46 100 44 Q128 46 126 80Z" fill="${K}"/><path d="M74 75 H126 V68 H74Z" fill="${C}"/></g>`;
  if(hat==='cowboy')s+=`<path d="M70 82 Q66 38 100 40 Q134 38 130 82Z" fill="#6B4A2B"/><path d="M30 66 Q60 94 100 92 Q140 94 170 66 Q146 82 100 80 Q54 82 30 66Z" fill="#6B4A2B"/><path d="M72 76 H128" stroke="${C}" stroke-width="4"/>`;
  if(hat==='headband')s+=`<path d="M70 92 Q100 82 130 92" stroke="${hcol==='bl'?acc:'#F4E6C8'}" stroke-width="8" fill="none"/>`;
  if(hat==='bandana')s+=`<path d="M68 100 Q66 64 100 62 Q134 64 132 100 Q100 86 68 100Z" fill="${acc}"/><path d="M130 88 L156 76 L152 104Z" fill="${acc}"/><g fill="${C}">${[[84,80],[100,76],[116,80],[92,88],[108,88]].map(([x,y])=>`<circle cx="${x}" cy="${y}" r="2"/>`).join('')}</g>`;
  if(hat==='cap')s+=`<path d="M68 90 Q70 56 100 54 Q130 56 132 90Z" fill="${ccol}"/><path d="M110 88 L162 94 Q152 102 112 98Z" fill="${ccol}"/>`;
  if(hat==='capback')s+=`<path d="M68 90 Q70 56 100 54 Q130 56 132 90Z" fill="${acc}"/><path d="M90 88 L38 94 Q48 102 88 98Z" fill="${acc}"/>`;
  if(hat==='cyclehelmet')s+=`<path d="M64 102 Q60 50 104 48 Q144 52 138 102 Q104 84 64 102Z" fill="${acc}"/><g stroke="${K}" stroke-width="3"><path d="M82 62 V86 M100 58 V86 M118 62 V86"/></g>`;
  if(hat==='swimcap')s+=`<path d="M66 100 Q62 54 100 52 Q138 54 134 100 Q100 86 66 100Z" fill="${acc}"/><circle cx="86" cy="92" r="9" fill="none" stroke="${C}" stroke-width="3"/><circle cx="114" cy="92" r="9" fill="none" stroke="${C}" stroke-width="3"/>`;
  if(hat==='tiara')s+=`<path d="M78 80 L82 62 L91 74 L100 56 L109 74 L118 62 L122 80Z" fill="#E8B93C"/><circle cx="100" cy="52" r="3.4" fill="#E8B93C"/>`;
  if(hat==='crown3')s+=`<path d="M64 34 L68 4 L84 22 L100 0 L116 22 L132 4 L136 34Z" fill="#E8B93C" stroke="${K}" stroke-width="2.4"/><g fill="#E8B93C">${[[68,2],[100,-2],[132,2]].map(([x,y])=>`<circle cx="${x}" cy="${y}" r="4.5"/>`).join('')}</g>`;
  if(hat==='fbhelmet')s+=`<path d="M64 108 Q58 50 100 48 Q142 50 136 108 L136 126 Q130 142 112 140 L104 126 L104 108Z" fill="${acc}" stroke="${K}" stroke-width="2.4"/><path d="M100 48 V104" stroke="${C}" stroke-width="5"/><g stroke="${C}" stroke-width="3.4" fill="none"><path d="M104 116 H134 M104 126 H132 M118 108 V134"/></g>`;
  if(hat==='headphones')s+=`<path d="M64 112 Q62 52 100 52 Q138 52 136 112" fill="none" stroke="${C}" stroke-width="6"/><rect x="56" y="104" width="14" height="28" rx="6" fill="${acc}"/><rect x="130" y="104" width="14" height="28" rx="6" fill="${acc}"/>`;
  if(hat==='spacehelmet')s+=`<circle cx="100" cy="112" r="64" fill="none" stroke="${C}" stroke-width="10"/><circle cx="100" cy="112" r="64" fill="${acc}" opacity=".13"/><path d="M60 92 Q100 64 140 92" stroke="#fff" stroke-width="4" fill="none" opacity=".6"/><rect x="82" y="168" width="36" height="22" rx="5" fill="${C}"/>`;
  /* accessoires au premier plan */
  if(has('headset'))s+=`<path d="M70 106 Q60 150 96 148" fill="none" stroke="${acc}" stroke-width="3"/><circle cx="96" cy="148" r="4.2" fill="${acc}"/>`;
  if(has('mic'))s+=`<g transform="rotate(-24 156 224)"><rect x="153" y="226" width="7" height="44" rx="3" fill="#7C7C86"/><circle cx="156.5" cy="214" r="14" fill="#B9B9C2"/><path d="M146 210 H167 M146 217 H167" stroke="#555" stroke-width="2"/></g>`;
  if(has('glove'))s+=`<g transform="translate(142 150) rotate(12)"><rect x="0" y="22" width="30" height="32" rx="9" fill="${C}"/>${[2,9,16,23].map(x=>`<rect x="${x}" y="0" width="6" height="30" rx="3" fill="${C}"/>`).join('')}<rect x="-5" y="34" width="12" height="9" rx="4" fill="${C}"/><g fill="${acc}"><circle cx="6" cy="8" r="2"/><circle cx="14" cy="26" r="2"/><circle cx="24" cy="12" r="2"/></g><rect x="2" y="52" width="26" height="10" fill="${acc}"/></g>`;
  if(has('boxing'))s+=`${[[48,206],[152,206]].map(([x,y])=>`<circle cx="${x}" cy="${y}" r="24" fill="#C62828" stroke="${K}" stroke-width="3"/><rect x="${x-14}" y="${y+18}" width="28" height="12" fill="${C}"/><path d="M${x-12} ${y-10} Q${x} ${y-18} ${x+12} ${y-10}" stroke="#fff" stroke-width="3" fill="none" opacity=".5"/>`).join('')}`;
  if(has('gkgloves'))s+=`${[[50,196],[150,196]].map(([x,y])=>`<circle cx="${x}" cy="${y}" r="20" fill="#7BD34E" stroke="${K}" stroke-width="3"/>${[-12,-4,4,12].map(d=>`<rect x="${x+d-2.5}" y="${y-30}" width="5" height="16" rx="2.5" fill="#7BD34E" stroke="${K}" stroke-width="1.6"/>`).join('')}`).join('')}`;
  if(has('ball'))s+=`<g transform="translate(152 262)"><circle r="26" fill="${C}" stroke="${K}" stroke-width="2.4"/><path d="M0 -10 L10 -3 L6 9 H-6 L-10 -3Z" fill="${K}"/><path d="M0 -10 V-26 M10 -3 L24 -8 M6 9 L14 22 M-6 9 L-14 22 M-10 -3 L-24 -8" stroke="${K}" stroke-width="2"/></g>`;
  if(has('racket'))s+=`<g transform="rotate(24 150 240)"><rect x="147" y="256" width="7" height="40" rx="3" fill="${C}"/><ellipse cx="150" cy="226" rx="22" ry="30" fill="none" stroke="${C}" stroke-width="5"/><path d="M150 196 V256 M128 226 H172 M134 210 H166 M134 242 H166" stroke="${C}" stroke-width="1.2" opacity=".7"/></g>`;
  if(has('bike'))s+=`<g fill="none" stroke="${C}" stroke-width="4"><circle cx="48" cy="276" r="26"/><circle cx="152" cy="276" r="26"/><path d="M48 276 L88 246 L152 276 M88 246 L124 246 M88 246 L100 230"/></g>`;
  if(has('guitar'))s+=`<g transform="rotate(-28 70 270)"><ellipse cx="70" cy="282" rx="32" ry="26" fill="#C98F4A"/><circle cx="70" cy="282" r="8" fill="${K}"/><rect x="66" y="196" width="8" height="70" fill="#6B4A2B"/></g>`;
  if(has('shoe'))s+=`<g transform="translate(120 252)"><path d="M0 30 Q0 8 22 8 L34 20 Q58 20 62 34 V40 H0Z" fill="${acc}"/><path d="M0 40 H62" stroke="${C}" stroke-width="5"/></g>`;
  if(has('club'))s+=`<g><path d="M156 140 L120 296" stroke="${C}" stroke-width="5"/><path d="M118 296 Q96 300 98 290 L120 288Z" fill="${C}"/><circle cx="168" cy="288" r="8" fill="${C}"/></g>`;
  if(has('blades'))s+=`<g fill="none" stroke="${C}" stroke-width="6" stroke-linecap="round"><path d="M50 236 Q58 270 40 292 Q68 298 76 282"/><path d="M150 236 Q142 270 160 292 Q132 298 124 282"/></g>`;
  if(has('case'))s+=`<g transform="translate(112 226)"><rect width="72" height="58" rx="6" fill="#3A3F4A" stroke="${C}" stroke-width="3"/><path d="M20 0 V-9 H52 V0" fill="none" stroke="${C}" stroke-width="4"/><rect x="30" y="22" width="12" height="10" fill="${acc}"/></g>`;
  if(has('cash'))s+=`<g>${[0,1,2].map(i=>`<rect x="${112+i*12}" y="${220-i*6}" width="50" height="26" rx="3" fill="#5A9A56" stroke="#2E5E2C" stroke-width="2" transform="rotate(${-10+i*14} ${137+i*12} ${233-i*6})"/>`).join('')}</g>`;
  if(has('coin'))s+=`<g transform="translate(142 236)"><circle r="24" fill="#E8B93C" stroke="#9A7414" stroke-width="3"/><path d="M-8 -12 H6 Q12 -12 12 -5 Q12 0 6 0 H-8 M-8 0 H8 Q14 0 14 7 Q14 12 8 12 H-8 M-3 -16 V16" stroke="#9A7414" stroke-width="3.4" fill="none"/></g>`;
  if(has('vial'))s+=`<g transform="translate(138 190)"><rect x="0" y="0" width="16" height="52" rx="5" fill="#CFE8E0" opacity=".9"/><rect x="0" y="22" width="16" height="30" rx="5" fill="#59B36B"/></g>`;
  if(has('knife'))s+=`<g transform="rotate(30 150 240)"><rect x="146" y="262" width="9" height="30" rx="3" fill="#222"/><path d="M146 262 V210 Q148 202 156 208 L155 262Z" fill="#D8DCE2"/></g>`;
  if(has('cig'))s+=`<path d="M104 140 L134 148" stroke="${C}" stroke-width="4" stroke-linecap="round"/><path d="M136 146 Q146 132 138 122 Q146 112 140 100" stroke="${C}" stroke-width="2.4" fill="none" opacity=".6"/>`;
  if(has('paint'))s+=`<g transform="translate(24 214) rotate(-30)"><rect x="0" y="0" width="8" height="64" rx="3" fill="#C98F4A"/><path d="M-3 0 H11 L8 -16 H0Z" fill="${acc}"/></g>`;
  if(has('flag'))s+=`<g transform="translate(150 190)"><rect x="0" y="0" width="3" height="80" fill="${C}"/><rect x="3" y="2" width="42" height="26" fill="#2A4A9A"/><g fill="${C}">${[0,1,2].map(i=>`<rect x="3" y="${6+i*7}" width="42" height="2.4"/>`).join('')}</g></g>`;
  if(has('sparkle')||has('star'))s+=`<g fill="${C}">${[[40,60,9],[160,86,7],[150,40,5]].map(([x,y,r])=>`<path d="M${x} ${y-r} L${x+r*.3} ${y-r*.3} L${x+r} ${y} L${x+r*.3} ${y+r*.3} L${x} ${y+r} L${x-r*.3} ${y+r*.3} L${x-r} ${y} L${x-r*.3} ${y-r*.3}Z"/>`).join('')}</g>`;
  if(has('slipper'))s+=`<path d="M138 262 Q150 244 168 254 L176 270 Q160 282 138 274Z" fill="#C62828" stroke="${K}" stroke-width="2"/>`;
  if(has('check'))s+=`<g transform="translate(112 234) rotate(-8)"><rect width="76" height="38" rx="3" fill="${C}"/><path d="M8 14 H46 M8 24 H34" stroke="${K}" stroke-width="3"/><text x="70" y="30" text-anchor="end" font-family="Arial" font-weight="bold" font-size="14" fill="#2E7D32">$</text></g>`;
  return s;
}
function hsl(h,s,l){const a=s*Math.min(l,1-l),f=k=>{const x=(k+h/30)%12;return Math.round(255*(l-a*Math.max(-1,Math.min(x-3,9-x,1)))).toString(16).padStart(2,'0');};return '#'+f(0)+f(8)+f(4);}
let n=0;
P.forEach(sp=>{
  const old=covers[sp[0]];if(!old)return;
  const hue=(n*47+20)%360;const c0=hsl(hue,.62,.42);
  const acc=c0;
  const bg=`<defs><linearGradient id="gP" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c0}"/><stop offset=".6" stop-color="${shade(c0,.45)}"/><stop offset="1" stop-color="#070506"/></linearGradient><radialGradient id="zP" cx=".5" cy=".38" r=".6"><stop offset="0" stop-color="#fff" stop-opacity=".34"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs><rect width="200" height="300" fill="url(#gP)"/><rect width="200" height="300" fill="url(#zP)"/><circle cx="100" cy="112" r="84" fill="${C}" opacity=".16"/>`;
  covers[sp[0]]=`<svg viewBox="0 0 200 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true">${bg}${figure(sp,acc)}</svg>`;n++;
});
fs.writeFileSync(path.join(root,'data/covers.json'),JSON.stringify(covers));
console.log('portraits',n);
