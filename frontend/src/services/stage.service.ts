import { Injectable } from '@angular/core';
import { Headers, RequestOptions, Http } from '@angular/http';

import { Stage } from '../models/stage';

const mocking = process.env.ENV !== 'production';
const apiBase = mocking ? '/app' : '/api/v1';

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

    toggleStatus(stage: Stage) {
        let url = `${apiBase}/stages/${stage.id}`;
        let body = JSON.stringify(stage);
        let headers: Headers = new Headers({ 'Content-Type': 'application/json' });
        let options = new RequestOptions({ headers: headers });
        return this.http.put(url, body, options)
            .toPromise()
            .then(response => response)
            .catch(this.handleError);
    }

    private handleError(error: any) {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    }
}
