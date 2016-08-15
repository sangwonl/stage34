import { Component, OnInit, ViewChild } from '@angular/core';
import { Response } from '@angular/http';

import { StageService } from '../../services/stage.service';
import { NavBarComponent } from '../nav/nav-bar.component';

import { StageCardComponent } from './card/stage-card.component';
import { StageInfoComponent } from '../modals/stage-info.component';
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

    onStageStatusClicked(event: any) {
        let stage: Stage = event.value;
        let stageId: number = stage.id;

        let statusMap: any = {'running': 'paused', 'paused': 'running'};
        let stageCopy: Stage = Object.assign({}, stage);
        stageCopy.status = statusMap[stage.status];

        this.stageService.toggleStatus(stageCopy).then((response: Response) => {
            console.log(response);
            stage.status = stageCopy.status;
        });
    }

    onStageNewClicked(event: any) {
        alert('sss'); 
    }
}