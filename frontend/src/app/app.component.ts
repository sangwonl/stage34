import { Component, ViewContainerRef } from '@angular/core';
import { ComponentsHelper } from 'ng2-bootstrap/components/utils/components-helper.service';

import { DashComponent } from './components/dash/dash.component';
import { LoginComponent } from './components/auth/login.component';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss']
})
export class AppComponent {
  private viewContainerRef: ViewContainerRef;

  public constructor(componentsHelper: ComponentsHelper, viewContainerRef: ViewContainerRef) {
    componentsHelper.setRootViewContainerRef(viewContainerRef)
  }
}
