import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';

import { AuthService } from './auth.service';
import { Stage } from '../models/stage';
import { Repo, Branch } from '../models/repo';

import { STAGE34_API_BASE } from '../consts';

@Injectable()
export class StageService {
    constructor(private authService: AuthService, private http: Http) {}

    private setAuthorizationHeader(headers: Headers) {
        headers.append('Authorization', `token ${this.authService.getToken()}`);
    }

    public getStages() {
        let url = `${STAGE34_API_BASE}/stages/`;
        let headers = new Headers();
        this.setAuthorizationHeader(headers);
        return this.http.get(url, { headers: headers })
            .toPromise()
            .then(response => response.json().data as Stage[]) 
            .catch(this.handleError);
    }

    public getStage(id: number) {
        let url = `${STAGE34_API_BASE}/stages/${id}/`;
        let headers = new Headers();
        this.setAuthorizationHeader(headers);
        return this.http.get(url, { headers: headers })
            .toPromise()
            .then(response => response.json().data as Stage)
            .catch(this.handleError);
    }

    public createStage(stageInfo: any) {
        let newStage = new Stage(
            stageInfo.title, 
            stageInfo.repo.full_name, 
            stageInfo.branch.name,
            stageInfo.repo.default_branch, 
            stageInfo.runOnClose
        );

        let url = `${STAGE34_API_BASE}/stages/`;
        let body = JSON.stringify(newStage);
        let headers: Headers = new Headers({ 'Content-Type': 'application/json' });
        this.setAuthorizationHeader(headers);
        return this.http.post(url, body, { headers: headers })
            .toPromise()
            .then(response => response.json().data as Stage)
            .catch(this.handleError);
    }

    public deleteStage(stage: Stage) {
        let url = `${STAGE34_API_BASE}/stages/${stage.id}/`;
        let headers: Headers = new Headers({ 'Content-Type': 'application/json' });
        this.setAuthorizationHeader(headers);
        return this.http.delete(url, { headers: headers })
            .toPromise()
            .then(response => {})
            .catch(this.handleError);       
    }

    public toggleStatus(stage: Stage) {
        let statusToggleMap: any = {'running': 'paused', 'paused': 'running'};
        let stageCopy: Stage = Object.assign({}, stage);
        stageCopy.status = statusToggleMap[stage.status];

        let url = `${STAGE34_API_BASE}/stages/${stage.id}/`;
        let body = JSON.stringify(stageCopy);
        let headers: Headers = new Headers({ 'Content-Type': 'application/json' });
        this.setAuthorizationHeader(headers);
        return this.http.put(url, body, { headers: headers })
            .toPromise()
            .then(response => {})
            .catch(this.handleError);
    }

    private handleError(error: any) {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    }
}
