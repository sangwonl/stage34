import { bootstrap } from '@angular/platform-browser-dynamic';
import { enableProdMode } from '@angular/core';
import { disableDeprecatedForms, provideForms } from '@angular/forms';

import { HTTP_PROVIDERS, XHRBackend } from '@angular/http';
import { appRouterProviders } from './routes/app.routes';

import { AppComponent } from './app/app.component';
import { AuthService } from './services/auth.service';
import { AuthGuard, AnonymousGuard } from './services/guard.service';

import { InMemoryBackendService, SEED_DATA } from 'angular2-in-memory-web-api';
import { InMemoryDataService } from './services/in-memory-data.service'; 

if (process.env.ENV === 'production') {
     enableProdMode();
}

bootstrap(AppComponent, [
    HTTP_PROVIDERS,
    AuthService,
    AuthGuard,
    AnonymousGuard,
    appRouterProviders,
    disableDeprecatedForms(),
    provideForms(),
    // { provide: XHRBackend, useClass: InMemoryBackendService },
    // { provide: SEED_DATA, useClass: InMemoryDataService }
]);
