import { ModuleWithProviders } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AuthGuard, AnonymousGuard } from './services/guard.service';
import { LoginComponent } from './components/auth/login.component';
import { DashComponent } from './components/dash/dash.component';

const appRoutes: Routes = [
  { path: '', redirectTo: '/dash', pathMatch: 'full'},
  { path: 'dash', component: DashComponent, canActivate: [AuthGuard] },
  { path: 'login', component: LoginComponent, canActivate: [AnonymousGuard] }
];

export const AppRouteModule: ModuleWithProviders = RouterModule.forRoot(appRoutes);
