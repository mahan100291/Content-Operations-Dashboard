import { NextResponse, type NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const goRouteMatch = request.nextUrl.pathname.match(/^\/go\/([^/]+)$/);

  if (goRouteMatch) {
    const url = request.nextUrl.clone();
    const workspace = decodeURIComponent(goRouteMatch[1]);

    url.pathname = '/';
    url.searchParams.set('workspace', workspace);

    const response = NextResponse.rewrite(url);
    response.headers.set('x-content-workspace', workspace);

    return response;
  }

  const response = NextResponse.next();
  const workspace = request.nextUrl.searchParams.get('workspace');

  if (workspace) {
    response.headers.set('x-content-workspace', workspace);
  }

  return response;
}

export const config = {
  matcher: ['/', '/go/:workspace'],
};
