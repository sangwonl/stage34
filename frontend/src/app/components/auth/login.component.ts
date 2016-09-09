import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../../services/auth.service';
import { GithubService } from '../../services/github.service';
import { CookieService } from 'angular2-cookie/core';

@Component({
    selector: 'login',
    templateUrl: 'login.component.html',
    styleUrls: ['login.component.css']
})
export class LoginComponent implements OnInit {
    private loginInProgress: boolean = false;
    private primaryEmail: string;

    constructor(
        private authService: AuthService,
        private githubService: GithubService,
        private cookieService: CookieService,
        private router: Router
    ) {}

    ngOnInit() {
        let githubAccessToken = this.cookieService.get('github-access-token');
        if (githubAccessToken && githubAccessToken.length > 0) {
            this.loginInProgress = true;
            this.githubService.setAccessToken(githubAccessToken);
            this.githubService.getPrimaryEmail().then(email => {
                this.primaryEmail = email;
            });
        }
    }

    private login() {
        this.authService.login();
    }

    private confirm() {
        let githubAccessToken = this.githubService.getAccessToken();
        this.authService.confirm(this.primaryEmail, githubAccessToken).then(loginDone => {
            if (loginDone) {
                this.cookieService.remove('github-access-token');
                this.router.navigate(['/dash']); 
            }
        });
    }
}
