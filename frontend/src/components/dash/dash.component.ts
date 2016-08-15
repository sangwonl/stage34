import { Component, OnInit, ViewChild } from '@angular/core';

import { StageService } from '../../services/stage.service';
import { NavBarComponent } from '../nav/nav-bar.component';

import { StageCardComponent } from './card/stage-card.component';
import { StageInfoComponent } from '../modals/stage-info.component';
import { StageNewComponent } from '../modals/stage-new.component';
import { Stage } from '../../models/Stage';

@Component({
    selector: 'dashboard',
    templateUrl: 'dash.component.html',
    styleUrls: ['dash.component.css'],
    providers: [StageService],
    directives: [
        NavBarComponent,
        StageCardComponent,
        StageInfoComponent,
        StageNewComponent
    ]
})
export class DashComponent implements OnInit {
    @ViewChild('stageInfoModal') stageInfoModal: StageInfoComponent;
    @ViewChild('stageNewModal') stageNewModal: StageNewComponent;
    stages: Stage[];

    constructor(private stageService: StageService) {}

    ngOnInit() {
        this.refreshStages();
    }

    refreshStages() {
        this.stageService.getStages()
            .then(stages => this.stages = stages);
    }

    onShowStageInfo(event: any) {
        this.stageInfoModal.showModal(event.value);
    }

    onToggleStageStatus(event: any) {
        let stage: Stage = event.value;
        let stageId: number = stage.id;

        let statusMap: any = {'running': 'paused', 'paused': 'running'};
        let stageCopy: Stage = Object.assign({}, stage);
        stageCopy.status = statusMap[stage.status];

        this.stageService.toggleStatus(stageCopy).then(response => {
            console.log(response);
            stage.status = stageCopy.status;
        });
    }

    onAddNewStage(event: any) {
        this.stageNewModal.showModal();
    }

    onCreateNewStage(event: any) {
        let newStageInfo = event.value;
        let runOnClose = newStageInfo.runOnClose;
        delete newStageInfo['runOnClose'];

        this.stageService.createStage(newStageInfo).then(stage => {
            console.log(stage); 
            this.refreshStages();
        })
    }
}