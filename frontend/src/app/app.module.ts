import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { Ng2BootstrapModule } from 'ng2-bootstrap/ng2-bootstrap';

import { AppComponent } from './app.component';
import { NavBarComponent } from './components/nav/nav-bar.component';
import { LoginComponent } from './components/auth/login.component';
import { DashComponent } from './components/dash/dash.component';
import { StageCardComponent } from './components/dash/card/stage-card.component';
import { StageInfoComponent } from './components/modals/stage-info.component';
import { StageNewComponent } from './components/modals/stage-new.component';
import { AppRouteModule } from './app.routes';

import { CookieService } from 'angular2-cookie/core';
import { AuthService } from './services/auth.service';
import { AuthGuard, AnonymousGuard } from './services/guard.service';
import { GithubService } from './services/github.service';
import { StageService } from './services/stage.service';

import { TimeAgoPipe } from 'angular2-moment';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    Ng2BootstrapModule,
    AppRouteModule
  ],
  declarations: [
    AppComponent,
    NavBarComponent,
    LoginComponent,
    LoginComponent,
    DashComponent,
    StageCardComponent,
    StageInfoComponent,
    StageNewComponent,
    TimeAgoPipe
  ],
  providers: [
    CookieService,
    AuthService,
    AuthGuard,
    AnonymousGuard,
    GithubService,
    StageService
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule {}