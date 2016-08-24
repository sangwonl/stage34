import { Component, OnInit, ViewChild } from '@angular/core';

import { StageService } from '../../services/stage.service';
import { NavBarComponent } from '../nav/nav-bar.component';

import { StageCardComponent } from './card/stage-card.component';
import { StageInfoComponent } from '../modals/stage-info.component';
import { StageNewComponent } from '../modals/stage-new.component';
import { Stage } from '../../models/stage';

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
    private stages: Stage[];

    constructor(private stageService: StageService) {}

    ngOnInit() {
        this.refreshStages();
    }

    private refreshStages() {
        this.stageService.getStages()
            .then(stages => this.stages = stages);
    }

    private onShowStageInfo(event: any) {
        this.stageInfoModal.showModal(event.value);
    }

    private onToggleStageStatus(event: any) {
        let targetStage: Stage = event.value;
        this.stageService.toggleStatus(targetStage).then(stage => {
            targetStage.status = stage.status;   
            // this.refreshStages();
        });
    }

    private onAddNewStage(event: any) {
        this.stageNewModal.showModal();
    }

    private onCreateNewStage(event: any) {
        let newStageInfo = event.value;
        let runOnClose = newStageInfo.runOnClose;
        delete newStageInfo['runOnClose'];

        this.stageService.createStage(newStageInfo).then(stage => {
            this.refreshStages();
        })
    }

    private onTrashStage(event: any) {
        let targetStage: Stage = event.value;
        this.stageService.deleteStage(targetStage).then(stage => {
            this.stages = this.stages.filter(s => s !== stage);
            // this.refreshStages();
        })
    }
}