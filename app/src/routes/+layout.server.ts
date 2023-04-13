/** @type {import('./$types').LayoutServerLoad} */
export function load({ cookies }) {
  const token = cookies.get('token');
  return {
    token
  };
}
