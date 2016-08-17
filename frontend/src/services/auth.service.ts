import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';

import { Headers, RequestOptions, Http } from '@angular/http';

import 'rxjs/add/observable/of';
import 'rxjs/add/operator/do';
import 'rxjs/add/operator/delay';

const mocking = false;
const forProd = process.env.ENV === 'production';
const apiHost = forProd ? 'http://api.stage34.org': 'http://localhost:8000';
const apiBase = mocking ? '/app' : `${apiHost}/api/v1`;

@Injectable()
export class AuthService {
    isLoggedIn: boolean = false;

    constructor(private http: Http) {}

    isAuthenticated() {
        return this.isLoggedIn;
    }

    get_github_auth_url() {
        let url = `${apiBase}/auth/github_auth_url`;
        return this.http.get(url)
            .toPromise()
            .then(response => response.json().data) 
            .catch(this.handleError);        
    }

    redirect(url) {
        window.location.href = url;
    }

    login() {
        console.log(apiBase);
        this.get_github_auth_url().then(data => { this.redirect(data.authorize_url); });
        // let jwt = 'aaa';
        // localStorage.setItem('jwt', jwt);
        // this.router.navigate(['/home']);
        // return false;
        return Observable.of(true).delay(1000).do(val => this.isLoggedIn = false);
    }

    logout() {
        // localStorage.removeItem('jwt');
        // this.router.navigate(['/login']);
        this.isLoggedIn = false;
    }

    private handleError(error: any) {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    }
}