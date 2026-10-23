const base=import.meta.env.VITE_API_BASE_URL||'http://localhost:8000';
export async function api<T>(path:string,init:RequestInit={}):Promise<T>{const headers=new Headers(init.headers);headers.set('Content-Type','application/json');if(import.meta.env.VITE_USE_DEMO_AUTH!=='false')headers.set('X-Demo-Role','admin');const r=await fetch(base+path,{...init,headers});if(!r.ok)throw new Error(`API ${r.status}: ${await r.text()}`);return r.json() as Promise<T>}
Property 'env' does not exist on type 'ImportMeta'
