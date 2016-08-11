import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { NavBarComponent } from '../nav/nav.component';

@Component({
    selector: 'dashboard',
    templateUrl: 'dash.component.html',
    styleUrls: ['dash.component.css'],
    directives: [NavBarComponent]
})
export class DashComponent implements OnInit {
    constructor(private router: Router) {}

    ngOnInit() {}
}