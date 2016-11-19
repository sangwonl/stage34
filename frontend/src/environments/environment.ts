// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `angular-cli.json`.

const stage34_host = 'http://stage34.io:8000'

export const environment = {
  production: false,
  stage34_host_base: stage34_host,
  stage34_api_base: `${stage34_host}/api/v1`,
  github_api_base: 'https://api.github.com'
};
