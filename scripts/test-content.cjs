const fs = require('node:fs');
const path = require('node:path');
const katex = require('../assets/hub/vendor/katex/katex.min.js');
const root=path.resolve(__dirname,'..');
const articles=JSON.parse(fs.readFileSync(path.join(root,'content/articles.json'),'utf8'));
let count=0;
for(const article of articles){
 const html=fs.readFileSync(path.join(root,article.content),'utf8');
 for(const match of html.matchAll(/<div class="math">([\s\S]*?)<\/div>/g)){
  const math=match[1].replaceAll('&amp;','&').replaceAll('&lt;','<').replaceAll('&gt;','>');
  try{katex.renderToString(math,{throwOnError:true,displayMode:true});count++;}
  catch(error){throw new Error(`${article.slug}: ${error.message}`);}
 }
}
console.log(`Validated ${count} LaTeX expressions with the bundled KaTeX renderer.`);
