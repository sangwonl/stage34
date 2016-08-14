import { Component, OnInit } from '@angular/core';

import { StageService } from '../../services/stage.service';
import { NavBarComponent } from '../nav/nav-bar.component';

import { StageCardComponent } from './card/stage-card.component';
import { Stage } from '../../models/Stage';

@Component({
    selector: 'dashboard',
    templateUrl: 'dash.component.html',
    styleUrls: ['dash.component.css'],
    providers: [StageService],
    directives: [NavBarComponent, StageCardComponent]
})
export class DashComponent implements OnInit {
    stages: Stage[];

    constructor(private stageService: StageService) {}

    ngOnInit() {
        this.stageService.getStages().then(stages => this.stages = stages);
    }
}