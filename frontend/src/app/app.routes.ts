import { provideRouter, RouterConfig } from '@angular/router';

import { AuthGuard } from './auth/auth.guard';
import { AnonymousGuard } from './auth/anonymous.guard';
import { LoginComponent } from './auth/login.component';
import { DashComponent } from './dash/dash.component';

const routes: RouterConfig = [
    { path: '', redirectTo: '/dash', pathMatch: 'full'},
    { path: 'dash', component: DashComponent, canActivate: [AuthGuard] },
    { path: 'login', component: LoginComponent, canActivate: [AnonymousGuard] }
];

export const appRouterProviders = [
    provideRouter(routes)
];
