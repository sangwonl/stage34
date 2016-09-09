import { Component, ViewContainerRef } from '@angular/core';

import { DashComponent } from './components/dash/dash.component';
import { LoginComponent } from './components/auth/login.component';

import '../../public/css/styles.css';

@Component({
    selector: 'stage34-app',
    templateUrl: 'app.component.html',
    styleUrls: ['app.component.css']
})
export class AppComponent {
    private viewContainerRef:ViewContainerRef;

    public constructor(viewContainerRef: ViewContainerRef) {
        this.viewContainerRef = viewContainerRef;
    }
}
