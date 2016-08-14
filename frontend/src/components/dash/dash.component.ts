import { Component, OnInit, ViewChild } from '@angular/core';

import { StageService } from '../../services/stage.service';
import { NavBarComponent } from '../nav/nav-bar.component';

import { StageCardComponent } from './card/stage-card.component';
import { StageInfoComponent } from './info/stage-info.component';
import { Stage } from '../../models/Stage';

@Component({
    selector: 'dashboard',
    templateUrl: 'dash.component.html',
    styleUrls: ['dash.component.css'],
    providers: [StageService],
    directives: [NavBarComponent, StageCardComponent, StageInfoComponent]
})
export class DashComponent implements OnInit {
    @ViewChild('stageInfoModal') stageInfoModal: StageInfoComponent;
    stages: Stage[];

    constructor(private stageService: StageService) {}

    ngOnInit() {
        this.stageService.getStages().then(stages => this.stages = stages);
    }

    onStageInfoClicked(event: any) {
        this.stageInfoModal.showModal(event.value);
    }
}