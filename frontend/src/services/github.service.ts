import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';

import { Headers, RequestOptions, Http } from '@angular/http';

import 'rxjs/add/observable/of';
import 'rxjs/add/operator/do';
import 'rxjs/add/operator/delay';

import { GITHUB_API_BASE } from '../consts';

@Injectable()
export class GithubService {
    accessToken: string;

    constructor(private http: Http) {}

    setAccessToken(accessToken: string) {
        this.accessToken = accessToken;
    }

    setAuthorizationHeader(headers: Headers) {
        headers.append('Authorization', `token ${this.accessToken}`);
    }

    getPrimaryEmail() {
        let url = `${GITHUB_API_BASE}/user/emails`;
        let headers = new Headers();
        this.setAuthorizationHeader(headers);
        return this.http.get(url, { headers: headers })
            .toPromise()
            .then(response => response.json().filter((e: any) => e.primary)[0].email)
            .catch(this.handleError);
    }

    private handleError(error: any) {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    }
}