import { bootstrap } from '@angular/platform-browser-dynamic';
import { enableProdMode } from '@angular/core';

import { HTTP_PROVIDERS } from '@angular/http';
import { appRouterProviders } from './app/app.routes';

import { AppComponent } from './app/app.component';
import { AuthService } from './app/auth/auth.service';
import { AuthGuard } from './app/auth/auth.guard';
import { AnonymousGuard } from './app/auth/anonymous.guard';

if (process.env.ENV === 'production') {
     enableProdMode();
}

bootstrap(AppComponent, [
    HTTP_PROVIDERS,
    AuthService,
    AuthGuard,
    AnonymousGuard,
    appRouterProviders
]);
