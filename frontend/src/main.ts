import { bootstrap } from '@angular/platform-browser-dynamic';
import { enableProdMode } from '@angular/core';

import { HTTP_PROVIDERS } from '@angular/http';
import { appRouterProviders } from './routes/app.routes';

import { AppComponent } from './app/app.component';
import { AuthService } from './services/auth.service';
import { AuthGuard, AnonymousGuard } from './services/guard.service';

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
