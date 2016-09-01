import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

import { AuthService } from './auth.service';

@Injectable()
export class AuthGuard implements CanActivate {
    constructor(private authService: AuthService, private router: Router) {}

    public canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
        if (this.authService.isAuthenticated()) { return true; }

        // Store the attempted URL for redirecting
        this.authService.redirectUrl = state.url;

        // Navigate to the login page
        this.router.navigate(['/login']);

        // Guard user going to next
        return false;
    }
}

@Injectable()
export class AnonymousGuard implements CanActivate {
    constructor(private authService: AuthService, private router: Router) {}

    public canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
        if (!this.authService.isAuthenticated()) { return true; }

        // Navigate to the home page
        this.router.navigate(['/']);

        // Guard user going to next
        return false;
    }
}
