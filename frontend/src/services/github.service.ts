import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';

import { Http, Headers, URLSearchParams } from '@angular/http';

import { Repo } from '../models/repo';

import { GITHUB_API_BASE } from '../consts';

@Injectable()
export class GithubService {
    constructor(private http: Http) {}

    public setAccessToken(accessToken: string) {
        localStorage.setItem('github_access_token', accessToken);
    }

    public getAccessToken() {
        return localStorage.getItem('github_access_token');
    }

    private setAuthorizationHeader(headers: Headers) {
        headers.append('Authorization', `token ${this.getAccessToken()}`);
    }

    public getPrimaryEmail() {
        let url = `${GITHUB_API_BASE}/user/emails`;
        let headers = new Headers();
        this.setAuthorizationHeader(headers);
        return this.http.get(url, { headers: headers })
            .toPromise()
            .then(response => response.json().filter((e: any) => e.primary)[0].email)
            .catch(this.handleError);
    }

    public getRepositories() {
        let url = `${GITHUB_API_BASE}/user/repos`;
        let params = new URLSearchParams()
        params.set('sort', 'updated');
        params.set('direction', 'desc');

        let headers = new Headers();
        this.setAuthorizationHeader(headers);
        return this.http.get(url, { headers: headers, search: params })
            .toPromise()
            .then(response => response.json().map((r: any) => new Repo(r)))
            .catch(this.handleError);
    }

    private handleError(error: any) {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    }
}