const base = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export async function api<T>(
  path: string,
  init: RequestInit = {}
): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set('Content-Type', 'application/json');

  if (import.meta.env.VITE_USE_DEMO_AUTH !== 'false') {
    headers.set('X-Demo-Role', 'admin');
  }

  const response = await fetch(base + path, {
    ...init,
    headers,
  });

  if (!response.ok) {
    throw new Error(`API ${response.status}: ${await response.text()}`);
  }

  return response.json() as Promise<T>;
}

