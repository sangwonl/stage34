import { Injectable } from '@angular/core';
import { Headers, RequestOptions, Http } from '@angular/http';

import { Stage } from '../models/stage';

const mocking = false;
const forProd = process.env.ENV === 'production';
const apiHost = forProd ? 'http://api.stage34.org': 'http://localhost:8000';
const apiBase = mocking ? '/app' : `${apiHost}/api/v1`;

@Injectable()
export class StageService {
    constructor(private http: Http) {}

    getStages() {
        let url = `${apiBase}/stages`;
        return this.http.get(url)
            .toPromise()
            .then(response => response.json().data as Stage[]) 
            .catch(this.handleError);
    }

    getStage(id: number) {
        let url = `${apiBase}/stages/${id}`;
        return this.http.get(url)
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
        stage.connect_info = 'not provisioned yet';
        return stage;
    }

    createStage(stageInfo: any) {
        let newStage = this.newStage(stageInfo.title, stageInfo.repo, stageInfo.branch); 
        let url = `${apiBase}/stages`;
        let body = JSON.stringify(newStage);
        let headers: Headers = new Headers({ 'Content-Type': 'application/json' });
        let options = new RequestOptions({ headers: headers });
        return this.http.post(url, body, options)
            .toPromise()
            .then(response => response.json().data as Stage)
            .catch(this.handleError);
    }

    deleteStage(stage: Stage) {
        let url = `${apiBase}/stages/${stage.id}`;
        let headers: Headers = new Headers({ 'Content-Type': 'application/json' });
        let options = new RequestOptions({ headers: headers });
        return this.http.delete(url, options)
            .toPromise()
            .then(response => { return response.status == 204 ? stage : null; })
            .catch(this.handleError);       
    }

    toggleStatus(stage: Stage) {
        let statusToggleMap: any = {'running': 'paused', 'paused': 'running'};
        let stageCopy: Stage = Object.assign({}, stage);
        stageCopy.status = statusToggleMap[stage.status];

        let url = `${apiBase}/stages/${stage.id}`;
        let body = JSON.stringify(stageCopy);
        let headers: Headers = new Headers({ 'Content-Type': 'application/json' });
        let options = new RequestOptions({ headers: headers });
        return this.http.put(url, body, options)
            .toPromise()
            .then(response => { return response.status == 204 ? stageCopy : stage; })
            .catch(this.handleError);
    }

    private handleError(error: any) {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    }
}
