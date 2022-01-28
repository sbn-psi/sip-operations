#!/usr/bin/env bash
set -e

TOOL_PATH=~/git/archive-maintenance/sip-operations/

OLD_DIR=$1
NEW_DIR=$2
DEST_DIR=$NEW_DIR/deltas
BUNDLE_ID=gbo.ast.catalina_survey



mkdir -p $DEST_DIR

echo "sip delta"
$TOOL_PATH/sipdelta.py --old_sip $OLD_DIR/$BUNDLE_ID_*_*_sip_v1.0.tab --sip $NEW_DIR/$BUNDLE_ID_*_*_sip_v1.0.tab --dest $DEST_DIR
echo "transfer manifest delta"
$TOOL_PATH/transferdelta.py --transfer $NEW_DIR/$BUNDLE_ID_*_*_transfer_manifest_v1.0.tab --old_transfer $OLD_DIR/$BUNDLE_ID_*_*_transfer_manifest_v1.0.tab --dest $DEST_DIR
echo "checksum manifest delta"
$TOOL_PATH/checksumdelta.py --checksum $NEW_DIR/$BUNDLE_ID_*_*_checksum_manifest_v1.0.tab --old_checksum $OLD_DIR/$BUNDLE_ID_*_*_checksum_manifest_v1.0.tab --dest $DEST_DIR
echo "new aip label"
$TOOL_PATH/aiplabel.py --transfer $DEST_DIR/$BUNDLE_ID_*_*_transfer_manifest_v1.0.tab --checksum $DEST_DIR/$BUNDLE_ID_*_*_checksum_manifest_v1.0.tab --label $NEW_DIR/$BUNDLE_ID_*_*_aip_v1.0.xml --dest $DEST_DIR
echo "new sip label"
$TOOL_PATH/siplabel.py --sip $DEST_DIR/$BUNDLE_ID_*_*_sip_v1.0.tab --aiplabel $DEST_DIR/$BUNDLE_ID_*_*_aip_v1.0.xml --label $NEW_DIR/$BUNDLE_ID_*_*_sip_v1.0.xml --dest $DEST_DIR
