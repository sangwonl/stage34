import { Component, ViewChild, AfterViewInit } from '@angular/core';
import { ModalDirective } from 'ng2-bootstrap';

import { Stage } from '../../models/stage';

@Component({
    selector: 'stage-info',
    templateUrl: 'stage-info.component.html',
    styleUrls: ['stage-info.component.css']
})
export class StageInfoComponent implements AfterViewInit {
    @ViewChild('infoModal') infoModal: ModalDirective;
    private stage: Stage;
 
    ngAfterViewInit() {}

    public showModal(stage: Stage) {
        this.stage = stage;
        this.infoModal.show();
    }

    public hideModal() { this.infoModal.hide(); }
}