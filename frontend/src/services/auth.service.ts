import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';

import { Headers, RequestOptions, Http } from '@angular/http';

import 'rxjs/add/observable/of';
import 'rxjs/add/operator/do';
import 'rxjs/add/operator/delay';

import { User } from '../models/user';
import { STAGE34_API_BASE } from '../consts';

@Injectable()
export class AuthService {
    isLoggedIn: boolean = false;
    redirectUrl: string;

    constructor(private http: Http) {}

    isAuthenticated() {
        return this.isLoggedIn;
    }

    newUser(email: string, accessToken: string): User {
        let user = new User;
        user.email = email;
        user.access_token = accessToken;
        return user;
    }

    get_github_auth_url() {
        let url = `${STAGE34_API_BASE}/auth/github_auth_url`;
        return this.http.get(url)
            .toPromise()
            .then(response => response.json().data) 
            .catch(this.handleError);        
    }

    post_signin(email: string, accessToken: string) {
        let newUser = this.newUser(email, accessToken);
        let url = `${STAGE34_API_BASE}/auth/signin`;
        let body = JSON.stringify(newUser);
        let headers: Headers = new Headers({ 'Content-Type': 'application/json' });
        let options = new RequestOptions({ headers: headers });
        return this.http.post(url, body, options)
            .toPromise()
            .then(response => response.json().data)
            .catch(this.handleError);
    }

    redirect(url: string) {
        window.location.href = url;
    }

    login() {
        this.get_github_auth_url().then(data => { this.redirect(data.authorize_url); });
    }

    confirm(email: string, accessToken: string) {
        return this.post_signin(email, accessToken).then(data => data as User);
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