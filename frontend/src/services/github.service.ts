import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';

import { Http, Headers, URLSearchParams } from '@angular/http';

import { Stage } from '../models/stage';
import { Repo, Branch, Compare } from '../models/repo';

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
        params.set('per_page', '1000');

        let headers = new Headers();
        this.setAuthorizationHeader(headers);
        return this.http.get(url, { headers: headers, search: params })
            .toPromise()
            .then(response => response.json().map((r: any) => new Repo(r)))
            .catch(this.handleError);
    }

    public getBranches(repo: Repo) {
        let url = `${GITHUB_API_BASE}/repos/${repo.full_name}/branches`;
        let headers = new Headers();
        this.setAuthorizationHeader(headers);
        return this.http.get(url, { headers: headers })
            .toPromise()
            .then(response => response.json().map((b: any) => new Branch(b)))
            .catch(this.handleError);
    }

    public getCompareBranch(stage: Stage) {
        let url = `${GITHUB_API_BASE}/repos/${stage.repo}/compare/${stage.default_branch}...${stage.branch}`
        console.log(url);
        let headers = new Headers();
        this.setAuthorizationHeader(headers);
        return this.http.get(url, { headers: headers })
            .toPromise()
            .then(response => new Compare(response.json()))
            .catch(this.handleError);
    }

    private handleError(error: any) {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    }
}