import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../../services/auth.service';
import { GithubService } from '../../services/github.service';
import { CookieService } from 'angular2-cookie/core';

import { User } from '../../models/user';

@Component({
    selector: 'login',
    templateUrl: 'login.component.html',
    styleUrls: ['login.component.css'],
    providers: [CookieService, GithubService]
})
export class LoginComponent implements OnInit {
    loginInProgress: boolean = false;
    primaryEmail: string;
    accessToken: string;

    constructor(
        private authService: AuthService,
        private githubService: GithubService,
        private cookieService: CookieService,
        private router: Router
    ) {}

    ngOnInit() {
        this.accessToken = this.cookieService.get('github-access-token');
        if (this.accessToken && this.accessToken.length > 0) {
            this.githubService.setAccessToken(this.accessToken);
            this.githubService.getPrimaryEmail().then(email => {
                this.primaryEmail = email;
                this.loginInProgress = true;
            });
        }
    }

    login() {
        this.authService.login();
    }

    confirm() {
        this.authService.confirm(this.primaryEmail, this.accessToken).then((user: User) => {
            console.log(user);
            this.router.navigate(['/dash']); 
        });
    }
}
