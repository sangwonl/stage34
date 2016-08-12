import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';

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
        let url = `${apiBase}/${id}`;
        return this.http.get(url)
            .toPromise()
            .then(response => response.json().data as Stage)
            .catch(this.handleError);
    }

    private handleError(error: any) {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    }
}
