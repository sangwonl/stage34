import { Injectable } from '@angular/core';
import { Headers, RequestOptions, Http } from '@angular/http';

import { AuthService } from './auth.service';
import { Stage } from '../models/stage';

import { STAGE34_API_BASE } from '../consts';

@Injectable()
export class StageService {
    constructor(private authService: AuthService, private http: Http) {}

    setAuthorizationHeader(headers: Headers) {
        headers.append('Authorization', `token ${this.authService.getToken()}`);
    }

    getRequestOptions(headers: Headers) {
        return new RequestOptions({ headers: headers });
    }

    getStages() {
        let url = `${STAGE34_API_BASE}/stages/`;
        let headers = new Headers();
        this.setAuthorizationHeader(headers);
        return this.http.get(url, this.getRequestOptions(headers))
            .toPromise()
            .then(response => response.json().data as Stage[]) 
            .catch(this.handleError);
    }

    getStage(id: number) {
        let url = `${STAGE34_API_BASE}/stages/${id}/`;
        let headers = new Headers();
        this.setAuthorizationHeader(headers);
        return this.http.get(url, this.getRequestOptions(headers))
            .toPromise()
            .then(response => response.json().data as Stage)
            .catch(this.handleError);
    }

    newStage(title: string, repo: string, branch: string): Stage {
        let stage = new Stage;
        stage.title = title;
        stage.repo = repo;
        stage.branch = branch;
        stage.status = 'paused';
        stage.commits = 0;
        stage.created_ts = new Date().getTime();
        stage.endpoint = 'not provisioned yet';
        return stage;
    }

    createStage(stageInfo: any) {
        let newStage = this.newStage(stageInfo.title, stageInfo.repo, stageInfo.branch); 
        let url = `${STAGE34_API_BASE}/stages/`;
        let body = JSON.stringify(newStage);
        let headers: Headers = new Headers({ 'Content-Type': 'application/json' });
        this.setAuthorizationHeader(headers);
        return this.http.post(url, body, this.getRequestOptions(headers))
            .toPromise()
            .then(response => response.json().data as Stage)
            .catch(this.handleError);
    }

    deleteStage(stage: Stage) {
        let url = `${STAGE34_API_BASE}/stages/${stage.id}/`;
        let headers: Headers = new Headers({ 'Content-Type': 'application/json' });
        this.setAuthorizationHeader(headers);
        return this.http.delete(url, this.getRequestOptions(headers))
            .toPromise()
            .then(response => { return response.status == 204 ? stage : null; })
            .catch(this.handleError);       
    }

    toggleStatus(stage: Stage) {
        let statusToggleMap: any = {'running': 'paused', 'paused': 'running'};
        let stageCopy: Stage = Object.assign({}, stage);
        stageCopy.status = statusToggleMap[stage.status];

        let url = `${STAGE34_API_BASE}/stages/${stage.id}/`;
        let body = JSON.stringify(stageCopy);
        let headers: Headers = new Headers({ 'Content-Type': 'application/json' });
        this.setAuthorizationHeader(headers);
        return this.http.put(url, body, this.getRequestOptions(headers))
            .toPromise()
            .then(response => { return response.status == 204 ? stageCopy : stage; })
            .catch(this.handleError);
    }

    private handleError(error: any) {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    }
}
