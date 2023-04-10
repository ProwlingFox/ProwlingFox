import { isJWTValid } from '$lib/requestUtils';
import { redirect } from '@sveltejs/kit';
import { page } from '$app/stores';

const publicPaths = [
  "/login",
  "/signup"
]


/** @type { import('./$types').LayoutLoad } */
export function load({ url }) {
  // allways allow access to public pages
  if ( publicPaths.includes(url.pathname) ) {
    return {

    }
  }

  if ( !isJWTValid() ) {
    throw redirect(301, '/login')
  }

  return {
      
  };
}