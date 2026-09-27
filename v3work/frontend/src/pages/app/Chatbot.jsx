import React,{useEffect,useRef,useState} from 'react'
import {api} from '../../api.js'
import {Panel} from '../../components/UI.jsx'
const tr=(T,k,f)=>T?.[k]||f
const SPEECH={'English':'en-IN','हिन्दी (Hindi)':'hi-IN','অসমীয়া (Assamese)':'as-IN','বাংলা (Bengali)':'bn-IN','ગુજરાતી (Gujarati)':'gu-IN','ಕನ್ನಡ (Kannada)':'kn-IN','മലയാളം (Malayalam)':'ml-IN','मराठी (Marathi)':'mr-IN','ଓଡ଼ିଆ (Odia)':'or-IN','ਪੰਜਾਬੀ (Punjabi)':'pa-IN','தமிழ் (Tamil)':'ta-IN','తెలుగు (Telugu)':'te-IN','اردو (Urdu)':'ur-IN','नेपाली (Nepali)':'ne-NP','संસ્કृत (Sanskrit)':'sa-IN','कोंकणी (Konkani)':'kok-IN','کٲشُر (Kashmiri)':'ks-IN','سنڌي (Sindhi)':'sd-IN','बोडो (Bodo)':'brx-IN','डोगरी (Dogri)':'doi-IN','मैथिली (Maithili)':'mai-IN','মৈতৈলোন (Meitei / Manipuri)':'mni-IN'}

function renderInline(text){
  const parts=String(text).split(/(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)/g)
  return parts.map((part,i)=>{
    if(part.startsWith('**')&&part.endsWith('**')) return <strong key={i}>{part.slice(2,-2)}</strong>
    if(part.startsWith('`')&&part.endsWith('`')) return <code key={i}>{part.slice(1,-1)}</code>
    if(part.startsWith('*')&&part.endsWith('*')) return <em key={i}>{part.slice(1,-1)}</em>
    return <React.Fragment key={i}>{part}</React.Fragment>
  })
}

function renderAssistantMessage(text){
  const lines=String(text||'').replace(/\r\n?/g,'\n').split('\n')
  const blocks=[]
  let list=[]
  const flushList=()=>{
    if(!list.length)return
    blocks.push(
      <ul className="assistant-list" key={`list-${blocks.length}`}>
        {list.map((item,i)=><li key={i}>{renderInline(item)}</li>)}
      </ul>
    )
    list=[]
  }
  lines.forEach((raw,i)=>{
    const line=raw.trim()
    if(!line){flushList();return}
    const bullet=line.match(/^[-•]\s+(.*)$/)
    const numbered=line.match(/^\d+[.)]\s+(.*)$/)
    if(bullet||numbered){
      list.push((bullet||numbered)[1])
      return
    }
    flushList()
    const heading=line.match(/^#{1,3}\s+(.*)$/)
    if(heading){
      blocks.push(<h4 className="assistant-heading" key={`h-${i}`}>{renderInline(heading[1])}</h4>)
      return
    }
    blocks.push(<p className="assistant-paragraph" key={`p-${i}`}>{renderInline(line)}</p>)
  })
  flushList()
  return <div className="assistant-content">{blocks}</div>
}

function plainForSpeech(text){
  return String(text||'')
    .replace(/#{1,6}\s+/g,'')
    .replace(/\*\*([^*]+)\*\*/g,'$1')
    .replace(/\*([^*]+)\*/g,'$1')
    .replace(/`([^`]+)`/g,'$1')
    .replace(/^[-•]\s+/gm,'')
    .replace(/^\d+[.)]\s+/gm,'')
}
export default function Chatbot({profile,site,language,T}){
 const [messages,setMessages]=useState([{role:'assistant',content:'Hello. I am the OIL-SIF Safety Assistant. Choose a question below or ask your own question in plain language.'}]),[input,setInput]=useState(''),[loading,setLoading]=useState(false),[listening,setListening]=useState(false);const ref=useRef(null)

useEffect(()=>{
  const stopSpeech=(e)=>{
    if(!e.target.closest('.read-button,.read-aloud-btn')){
      window.speechSynthesis?.cancel()
    }
  }

  document.addEventListener('click',stopSpeech)

  return()=>document.removeEventListener('click',stopSpeech)
},[])

 const suggestions=['What needs attention today?','Which activity has the highest SIF risk?','What are the main failed barrier patterns?','Summarise the current safety situation.','Explain Energy Isolation in simple language.']
 async function send(v){const q=(v??input).trim();if(!q||loading)return;setMessages(m=>[...m,{role:'user',content:q}]);setInput('');setLoading(true);try{const r=await api.chat(q);setMessages(m=>[...m,{role:'assistant',content:r.reply||'No answer was returned.'}])}catch(e){setMessages(m=>[...m,{role:'assistant',content:'The Safety Assistant is temporarily unavailable. Please use the dashboard data or try again.',error:true}])}finally{setLoading(false)}}
 function voice(){const SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR)return;const r=new SR();r.lang=SPEECH[language]||'en-IN';r.interimResults=true;r.onstart=()=>setListening(true);r.onresult=e=>{let t='';for(let i=e.resultIndex;i<e.results.length;i++)if(e.results[i].isFinal)t+=e.results[i][0].transcript+' ';if(t)setInput(v=>(v+' '+t).trim())};r.onend=()=>setListening(false);r.start();ref.current=r}
 function read(text){window.speechSynthesis?.cancel();const u=new SpeechSynthesisUtterance(text);u.lang=SPEECH[language]||'en-IN';window.speechSynthesis?.speak(u)}
 return <div className="copilot-page"><div className="copilot-hero"><div><span className="eyebrow">AI SAFETY ASSISTANT</span><h2>How can I help?</h2><p>Ask about SIF risk, recurring precursors, barriers, Life-Saving Rules or HSE priorities.</p></div><div className="copilot-context"><span>Signed in as</span><strong>{profile?.name}</strong><small>{profile?.role} · {site}</small></div></div>
 <Panel title="💡 Start with a question" subtitle="You can ask these in plain language."><div className="copilot-suggestions">{suggestions.map(x=><button key={x} onClick={()=>send(x)} disabled={loading}>{x}</button>)}</div></Panel>
 <Panel title="🤖 Conversation" subtitle="AI answers support HSE triage and should be validated before operational decisions."><div className="chat-window">{messages.map((m,i)=><div className={`chat-message ${m.role==='user'?'chat-user':'chat-assistant'}`} key={i}><div className="chat-avatar">{m.role==='user'?'👤':'🤖'}</div><div className={`chat-bubble ${m.error?'chat-error':''}`}><div>{m.role==='assistant'?renderAssistantMessage(m.content):m.content}</div>{m.role==='assistant'&&<button className="read-button" onClick={()=>read(plainForSpeech(m.content))}>🔊 Read aloud</button>}</div></div>)}{loading&&<div className="chat-message chat-assistant"><div className="chat-avatar">🤖</div><div className="chat-bubble chat-thinking">Checking the available safety information…</div></div>}</div><form className="chat-input-area" onSubmit={e=>{e.preventDefault();send()}}><button type="button" className={`voice-chat-btn ${listening?'listening':''}`} onClick={voice}>{listening?'⏹':'🎙️'}</button><input ref={ref} value={input} onChange={e=>setInput(e.target.value)} placeholder="Type your safety question here…" disabled={loading}/><button className="btn-primary" type="submit" disabled={loading||!input.trim()}>Send</button></form></Panel>
 <div className="copilot-notice"><strong>⚠️ Human validation is required</strong><p>AI recommendations support — not replace — qualified HSE judgement.</p></div>
 </div>
}
