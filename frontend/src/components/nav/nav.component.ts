import { Component, OnInit } from '@angular/core';
import { Router, ROUTER_DIRECTIVES } from '@angular/router';

@Component({
    selector: 'nav-bar',
    templateUrl: 'nav.component.html',
    styleUrls: ['nav.component.css'],
    directives: [ROUTER_DIRECTIVES]
})
export class NavBarComponent implements OnInit {
    constructor(private router: Router) {}

    ngOnInit() {}
}