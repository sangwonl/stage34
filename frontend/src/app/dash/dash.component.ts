import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector: 'dashboard',
    templateUrl: 'dash.component.html',
    styleUrls: ['dash.component.css']
})
export class DashComponent implements OnInit {
    constructor(protected router: Router) {}

    ngOnInit() {}
}