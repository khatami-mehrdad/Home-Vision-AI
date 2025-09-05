#!/usr/bin/env python3
"""
Test DeGirum initialization to identify the issue
"""
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_degirum_import():
    """Test if DeGirum can be imported"""
    try:
        import degirum as dg
        logger.info("✅ DeGirum imported successfully")
        return True
    except ImportError as e:
        logger.error(f"❌ DeGirum import failed: {e}")
        return False

def test_degirum_initialization():
    """Test DeGirum model initialization"""
    try:
        import degirum as dg
        
        # Try to load a model (this might fail without proper token/setup)
        logger.info("🔧 Attempting to initialize DeGirum model...")
        
        # This is likely where it fails - need proper DeGirum token and model
        model = dg.load_model("mobilenet_v2_ssd_coco--300x300_quant_n2x_orca1_1")
        logger.info("✅ DeGirum model loaded successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ DeGirum model initialization failed: {e}")
        logger.error(f"Exception type: {type(e).__name__}")
        return False

def test_opencv_basic():
    """Test basic OpenCV functionality"""
    try:
        import cv2
        logger.info("✅ OpenCV imported successfully")
        
        # Test with a simple image
        import numpy as np
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        logger.info(f"✅ Created test image: {test_image.shape}")
        
        return True
    except Exception as e:
        logger.error(f"❌ OpenCV test failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Testing DeGirum and dependencies...")
    
    # Test 1: DeGirum import
    logger.info("\n1. Testing DeGirum import...")
    degirum_import_ok = test_degirum_import()
    
    # Test 2: OpenCV basic functionality
    logger.info("\n2. Testing OpenCV...")
    opencv_ok = test_opencv_basic()
    
    # Test 3: DeGirum initialization (this will likely fail)
    logger.info("\n3. Testing DeGirum initialization...")
    degirum_init_ok = test_degirum_initialization()
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("📋 Test Results Summary:")
    logger.info(f"DeGirum Import: {'✅ PASS' if degirum_import_ok else '❌ FAIL'}")
    logger.info(f"OpenCV Basic: {'✅ PASS' if opencv_ok else '❌ FAIL'}")
    logger.info(f"DeGirum Init: {'✅ PASS' if degirum_init_ok else '❌ FAIL (Expected)'}")
    
    if not degirum_init_ok:
        logger.info("\n💡 Recommendation:")
        logger.info("The live stream is failing because DeGirum AI detection can't initialize.")
        logger.info("Options:")
        logger.info("1. Configure DeGirum properly with token and model")
        logger.info("2. Create a fallback mode that works without AI detection")
        logger.info("3. Use basic OpenCV-only streaming for now")
