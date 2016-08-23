import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';

import { Headers, RequestOptions, Http } from '@angular/http';

import 'rxjs/add/observable/of';
import 'rxjs/add/operator/do';
import 'rxjs/add/operator/delay';

import { User } from '../models/user';
import { STAGE34_HOST_BASE } from '../consts';

@Injectable()
export class AuthService {
    isLoggedIn: boolean = false;
    redirectUrl: string;

    constructor(private http: Http) {}

    public isAuthenticated() {
        let token = this.getToken();
        this.isLoggedIn = token !== null;
        return this.isLoggedIn;
    }

    public getToken() {
        return localStorage.getItem('token');
    }

    private newUser(email: string, accessToken: string): User {
        let user = new User;
        user.email = email;
        user.access_token = accessToken;
        return user;
    }

    private getGithubAuthUrl() {
        let url = `${STAGE34_HOST_BASE}/auth/github_auth_url/`;
        return this.http.get(url)
            .toPromise()
            .then(response => response.json().data) 
            .catch(this.handleError);        
    }

    private postLogin(email: string, accessToken: string) {
        let newUser = this.newUser(email, accessToken);
        let url = `${STAGE34_HOST_BASE}/auth/login/`;
        let body = JSON.stringify(newUser);
        let headers: Headers = new Headers({ 'Content-Type': 'application/json' });
        let options = new RequestOptions({ headers: headers });
        return this.http.post(url, body, options)
            .toPromise()
            .then(response => response.json().data as User)
            .catch(this.handleError);
    }

    public login() {
        this.getGithubAuthUrl().then(data => {
            // redirect to github authorize url
            window.location.href = data.authorize_url;
        });
    }

    public confirm(email: string, accessToken: string) {
        return this.postLogin(email, accessToken).then(user => {
            localStorage.setItem('token', user.token);
            this.isLoggedIn = true;
            return this.isLoggedIn;
        });
    }

    public logout() {
        localStorage.removeItem('token');
        this.isLoggedIn = false;
    }

    private handleError(error: any) {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    }
}