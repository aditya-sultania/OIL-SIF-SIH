import { TRANSLATIONS } from './translations.js'

const CACHE_PREFIX = 'oil_i18n_runtime_v8:'
const API_BASE = import.meta.env.VITE_API_BASE || '/api'
const NEVER_TRANSLATE = new Set(['OIL-SIF','SIF','HSE','AI','IOGP','LOTO','API','URL','ID','CSV','NLP','OSHA'])
const nodeSources = new Map()
const attrSources = new WeakMap()
const reverseTranslations = new Map()
const inFlight = new Map()

let suppressObserver = 0

function clean(value){return String(value ?? '').replace(/\s+/g,' ').trim()}

function staticMap(language){
  const en=TRANSLATIONS.English||{}
  const target=TRANSLATIONS[language]||{}
  const map=new Map()
  for(const [key,source] of Object.entries(en)){
    const translated=target[key]
    if(typeof source==='string' && typeof translated==='string' && clean(source) && clean(translated) && clean(source)!==clean(translated)){
      map.set(clean(source),translated)
    }
  }
  return map
}

function isUiNode(node){
  const parent=node.parentElement
  if(!parent)return false
  if(['SCRIPT','STYLE','NOSCRIPT','CODE','PRE','TEXTAREA','OPTION'].includes(parent.tagName))return false
  if(parent.closest('[data-no-i18n="true"]'))return false
  if(parent.closest('.user-copy,.report-narrative,.user-name,.chat-bubble,.my-report-body,.narrative-box'))return false
  const text=clean(node.nodeValue)
  if(!text||text.length>220)return false
  if(/^[\d\s.,:%+\-–—/()#]+$/.test(text))return false
  if(/^[A-Z0-9_-]{2,30}$/.test(text)&&! /\s/.test(text))return false
  if(NEVER_TRANSLATE.has(text))return false
  return /[A-Za-zÀ-ÿ]/.test(text)
}

function shouldTranslateAttribute(el,attr){
  if(el.closest('[data-no-i18n="true"]'))return false
  if(el.closest('.user-copy,.report-narrative,.user-name,.chat-bubble,.my-report-body,.narrative-box'))return false
  return ['placeholder','title','aria-label'].includes(attr)
}

async function requestMissing(language, missing){
  const unique=[...new Set(missing.map(clean).filter(Boolean))]
  if(!unique.length)return {}

  // Identical concurrent batches share one network/Gemini request.
  const requestKey=`${language}::${unique.slice().sort().join('\u0001')}`
  if(inFlight.has(requestKey))return inFlight.get(requestKey)

  const promise=(async()=>{
    const token=localStorage.getItem('oil_sif_token')
    const headers={'Content-Type':'application/json'}
    if(token)headers.Authorization=`Bearer ${token}`

    for(let attempt=0;attempt<2;attempt++){
      try{
        const res=await fetch(`${API_BASE}/i18n/translate`,{
          method:'POST',
          headers,
          body:JSON.stringify({language,texts:unique})
        })
        if(res.ok){
          const data=await res.json()
          return data.translations||{}
        }
      }catch(_){/* retry once while FastAPI finishes starting */}
      if(attempt===0)await new Promise(resolve=>setTimeout(resolve,500))
    }
    return {}
  })()

  inFlight.set(requestKey,promise)
  try{return await promise}finally{inFlight.delete(requestKey)}
}

async function translateBatch(language,texts){
  const unique=[...new Set(texts.map(clean).filter(Boolean))]
  if(!unique.length||language==='English')return Object.fromEntries(unique.map(x=>[x,x]))

  const key=CACHE_PREFIX+language
  let cached={}
  try{cached=JSON.parse(localStorage.getItem(key)||'{}')}catch(_){cached={}}

  const local=staticMap(language)
  const reverse=reverseTranslations.get(language)||new Map()
  Object.entries(cached).forEach(([source,translated])=>reverse.set(clean(translated),source))
  local.forEach((translated,source)=>reverse.set(clean(translated),source))
  reverseTranslations.set(language,reverse)

  const result={}
  const missing=[]
  for(const source of unique){
    if(local.has(source)){
      result[source]=local.get(source)
      cached[source]=local.get(source)
    }else if(cached[source]){
      result[source]=cached[source]
    }else{
      missing.push(source)
    }
  }

  if(missing.length){
    const translated=await requestMissing(language,missing)
    Object.assign(cached,translated)
    Object.entries(translated).forEach(([source,value])=>{
      if(typeof value==='string'&&value.trim())reverse.set(clean(value),source)
    })
  }

  try{localStorage.setItem(key,JSON.stringify(cached))}catch(_){}

  for(const source of unique){
    result[source]=result[source]||cached[source]||source
  }
  return result
}

export function restoreAll(){
  suppressObserver++
  try{
    document.querySelectorAll('*').forEach(el=>{
      const map=attrSources.get(el)
      if(map)for(const [attr,source] of map)el.setAttribute(attr,source)
    })
    const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT)
    let node
    while((node=walker.nextNode())){
      const source=nodeSources.get(node)
      if(source)node.nodeValue=source
    }
  }finally{
    suppressObserver--
  }
}

async function collectAndTranslate(language){
  if(language==='English'){restoreAll();return}

  const nodes=[],attrs=[],texts=[]
  const reverse=reverseTranslations.get(language)||new Map()
  const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT)
  let node

  while((node=walker.nextNode())){
    if(!isUiNode(node))continue
    const current=clean(node.nodeValue)
    const source=nodeSources.get(node)||reverse.get(current)||current
    nodeSources.set(node,source)
    nodes.push({node,source})
    texts.push(source)
  }

  document.querySelectorAll('input,textarea,[title],[aria-label]').forEach(el=>{
    for(const attr of ['placeholder','title','aria-label']){
      if(!el.hasAttribute(attr)||!shouldTranslateAttribute(el,attr))continue
      const current=clean(el.getAttribute(attr))
      if(!current)continue
      let map=attrSources.get(el)
      if(!map){map=new Map();attrSources.set(el,map)}
      const source=map.get(attr)||reverse.get(current)||current
      map.set(attr,source)
      attrs.push({el,attr,source})
      texts.push(source)
    }
  })

  if(!texts.length)return

  const map=await translateBatch(language,texts)

  // React may have replaced nodes while Gemini was running. Only write to
  // nodes that are still mounted, and suppress the observer while doing so.
  suppressObserver++
  try{
    for(const item of nodes){
      if(document.body.contains(item.node)){
        const translated=map[item.source]||item.source
        if(item.node.nodeValue!==translated)item.node.nodeValue=translated
      }
    }
    for(const item of attrs){
      if(document.body.contains(item.el)){
        const translated=map[item.source]||item.source
        if(item.el.getAttribute(item.attr)!==translated)item.el.setAttribute(item.attr,translated)
      }
    }
  }finally{
    suppressObserver--
  }
}

export function installLanguageObserver(language){
  if(language==='English'){
    restoreAll()
    window.__oilSifTranslationReady=Promise.resolve()
    window.__oilSifRestoreLanguage=restoreAll
    return()=>{}
  }

  let stopped=false
  let timer=null
  let pending=Promise.resolve()

  const collect=()=>{
    if(stopped||suppressObserver)return
    clearTimeout(timer)
    timer=setTimeout(()=>{
      if(stopped)return
      pending=pending.then(()=>collectAndTranslate(language)).catch(err=>{
        console.warn('[OIL-SIF] Interface translation pass failed:',err)
      })
      window.__oilSifTranslationReady=pending
    },300)
  }

  // Initial pass. The observer below handles later React renders/navigation.
  collect()

  const observer=new MutationObserver(()=>{
    if(!stopped&&!suppressObserver)collect()
  })
  observer.observe(document.body,{childList:true,subtree:true,characterData:true})

  window.__oilSifTranslationReady=pending
  window.__oilSifRestoreLanguage=restoreAll

  return()=>{
    stopped=true
    clearTimeout(timer)
    observer.disconnect()
    restoreAll()
  }
}
