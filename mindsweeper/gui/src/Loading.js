import React, { useState, useEffect } from 'react';
import { Spinner } from 'react-bootstrap';

function Loading() {
  return (
    <Spinner animation="grow" className="m-3" />
  );
}

export default Loading;
