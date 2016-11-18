import { Component, ViewContainerRef } from '@angular/core';

import { DashComponent } from './components/dash/dash.component';
import { LoginComponent } from './components/auth/login.component';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss']
})
export class AppComponent {
  private viewContainerRef: ViewContainerRef;

  public constructor(viewContainerRef: ViewContainerRef) {
    this.viewContainerRef = viewContainerRef;
  }
}
