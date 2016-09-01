import { provideRouter, RouterConfig } from '@angular/router';

import { AuthGuard, AnonymousGuard } from '../services/guard.service';
import { LoginComponent } from '../components/auth/login.component';
import { DashComponent } from '../components/dash/dash.component';

const routes: RouterConfig = [
    { path: '', redirectTo: '/dash', pathMatch: 'full'},
    { path: 'dash', component: DashComponent, canActivate: [AuthGuard] },
    { path: 'login', component: LoginComponent, canActivate: [AnonymousGuard] }
];

export const appRouterProviders = [provideRouter(routes)];
