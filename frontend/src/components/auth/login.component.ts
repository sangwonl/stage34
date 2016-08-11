import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
    selector: 'login',
    templateUrl: 'login.component.html',
    styleUrls: ['login.component.css']
})
export class LoginComponent implements OnInit {
    constructor(private authService: AuthService, private router: Router) {}

    ngOnInit() {}

    login() {
        this.authService.login().toPromise().then(() => { this.router.navigate(['/dash']); });
    }
}
