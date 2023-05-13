import adapter from '@sveltejs/adapter-node'
import { vitePreprocess } from '@sveltejs/kit/vite';


/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://github.com/sveltejs/svelte-preprocess
	// for more information about preprocessors
	// preprocess: [
	// 	preprocess({
	// 		defaults: {
	// 			script: 'typescript',
	// 		},
	// 		postcss: true,
	// 	}),
	// ],
	preprocess: [vitePreprocess()],


	kit: {
		adapter: adapter(),
		alias: {
			'$components/*': './src/components/*',
			'$interfaces/*': './src/interfaces/*',
		},
	},
}

export default config
