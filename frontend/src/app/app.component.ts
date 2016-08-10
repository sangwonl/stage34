import { Component } from '@angular/core';
import { ROUTER_DIRECTIVES }  from '@angular/router';

import { DashComponent } from './dash/dash.component';
import { LoginComponent } from './auth/login.component';

import '../../public/css/styles.css';

@Component({
    selector: 'stage34-app',
    directives: [LoginComponent, ROUTER_DIRECTIVES],
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css'],
    precompile: [
        DashComponent,
        LoginComponent
    ]
})
export class AppComponent {}
