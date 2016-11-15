import { Component, ViewChild, AfterViewInit } from '@angular/core';
import { ModalDirective } from 'ng2-bootstrap';

import { StageService } from '../../services/stage.service';

import { Stage } from '../../models/stage';

@Component({
    selector: 'stage-info',
    templateUrl: 'stage-info.component.html',
    styleUrls: ['stage-info.component.scss']
})
export class StageInfoComponent implements AfterViewInit {
    @ViewChild('infoModal') infoModal: ModalDirective;
    private stage: Stage;
    private logData: any;

    constructor(private stageService: StageService) {}
 
    ngAfterViewInit() {}

    public showModal(stage: Stage) {
        this.stage = stage;
        this.stageService.getStageLog(this.stage.id).then((logData: any) => {
            this.logData = logData;
            this.infoModal.show();
        }).catch((error: any) => {
            this.logData = null;
            this.infoModal.show();
        });
    }

    public hideModal() { this.infoModal.hide(); }
}