import { Component, OnInit } from '@angular/core';
import { Router, ROUTER_DIRECTIVES } from '@angular/router';

import { AuthService } from '../../services/auth.service';

@Component({
    selector: 'nav-bar',
    templateUrl: 'nav-bar.component.html',
    styleUrls: ['nav-bar.component.css'],
    directives: [ROUTER_DIRECTIVES]
})
export class NavBarComponent implements OnInit {
    constructor(
        private authService: AuthService,
        private router: Router
    ) {}

    ngOnInit() {}

    private onLogout() {
        this.authService.logout();
        this.router.navigate(['/login']);
    }
}