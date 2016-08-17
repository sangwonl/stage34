import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/of';
import 'rxjs/add/operator/do';
import 'rxjs/add/operator/delay';

@Injectable()
export class AuthService {
    constructor() {}

    isLoggedIn: boolean = false;

    redirectUrl: string;

    isAuthenticated() {
        return this.isLoggedIn;
    }

    login() {
        // let jwt = 'aaa';
        // localStorage.setItem('jwt', jwt);
        // this.router.navigate(['/home']);
        // return false;
        return Observable.of(true).delay(1000).do(val => this.isLoggedIn = true);
    }

    logout() {
        // localStorage.removeItem('jwt');
        // this.router.navigate(['/login']);
        this.isLoggedIn = false;
    }
}