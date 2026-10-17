export default {
  async fetch(request, env, _ctx) {
    const url = new URL(request.url);

    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };

    // Handle OPTIONS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // API proxy endpoint
    if (url.pathname === '/api/proxy') {
      if (request.method !== 'POST') {
        return new Response('Method not allowed', { status: 405, headers: corsHeaders });
      }

      try {
        const { targetUrl, method, body } = await request.json();
        const response = await fetch(targetUrl, {
          method,
          headers: { ...request.headers, 'Content-Type': 'application/json' },
          body: body ? JSON.stringify(body) : undefined,
        });

        const cloned = response.clone();
        const responseData = await cloned.text();

        // Cache in KV if API_CACHE binding exists
        if (env.API_CACHE) {
          const cacheKey = btoa(targetUrl);
          await env.API_CACHE.put(cacheKey, responseData, { expirationTtl: 60 });
        }

        return new Response(responseData, {
          status: response.status,
          headers: { ...corsHeaders, 'Content-Type': response.headers.get('Content-Type') || 'application/json' },
        });
      } catch (error) {
        return new Response(JSON.stringify({ error: error.message }), {
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }
    }

    // Default: serve static assets if ASSETS binding exists
    if (env.ASSETS) {
      return env.ASSETS.fetch(request);
    }

    return new Response(JSON.stringify({ status: 'PRISM 9 Edge Worker Operational' }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  },
};
