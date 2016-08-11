import { Component } from '@angular/core';
import { ROUTER_DIRECTIVES }  from '@angular/router';

import { DashComponent } from '../components/dash/dash.component';
import { LoginComponent } from '../components/auth/login.component';

import 'jquery';
import 'bootstrap-loader';
import 'font-awesome/css/font-awesome.css';
import 'bootstrap-social/bootstrap-social.css';

import '../../public/css/styles.css';

@Component({
    selector: 'stage34-app',
    templateUrl: 'app.component.html',
    styleUrls: ['app.component.css'],
    directives: [ROUTER_DIRECTIVES],
    precompile: [
        DashComponent,
        LoginComponent
    ]
})
export class AppComponent {}
