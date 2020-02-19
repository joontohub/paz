import numpy as np

from paz.core.ops import compute_iou
from paz.core.ops import compute_ious
from paz.core.ops import denormalize_box
from paz.core.ops import to_point_form
from paz.core.ops import to_center_form
from paz.core.ops import rotation_matrix_to_quaternion
from paz.core.ops import quaternion_to_rotation_matrix
from paz.core.ops import encode
from paz.core.ops import match
from paz.core.ops import decode
from paz.models.detection.utils import create_prior_boxes


boxes_B = np.array([[39, 63, 203, 112],
                    [49, 75, 203, 125],
                    [31, 69, 201, 125],
                    [50, 72, 197, 121],
                    [35, 51, 196, 110]])

boxes_A = np.array([[54, 66, 198, 114],
                    [42, 78, 186, 126],
                    [18, 63, 235, 135],
                    [18, 63, 235, 135],
                    [54, 72, 198, 120],
                    [36, 60, 180, 108]])

target = [0.48706725, 0.787838, 0.70033113, 0.70739083, 0.39040922]


affine_matrix = np.array(
    [[-0., -0.994522, 0.104528, 3.135854],
     [0., 0.104528, 0.994522, 29.835657],
     [-1., 0., 0., 0.],
     [0., 0., -0., 1.]])


quaternion_target = np.array([0.525483, -0.473147, 0.525483, 0.473147])

target_unique_matches = np.array([[238., 155., 306., 204.]])

target_prior_boxes = np.array([[0.013333334, 0.013333334, 0.1, 0.1],
                               [0.013333334, 0.013333334, 0.14142136, 0.14142136],
                               [0.013333334, 0.013333334, 0.14142136, 0.07071068],
                               [0.013333334, 0.013333334, 0.07071068, 0.14142136],
                               [0.04, 0.013333334, 0.1, 0.1],
                               [0.04, 0.013333334, 0.14142136, 0.14142136],
                               [0.04, 0.013333334, 0.14142136, 0.07071068],
                               [0.04, 0.013333334, 0.07071068, 0.14142136],
                               [0.06666667, 0.013333334, 0.1, 0.1],
                               [0.06666667, 0.013333334, 0.14142136, 0.14142136]],
                              dtype=np.float32)

boxes_with_label = np.array([[47., 239., 194., 370.,  12.],
                            [7.,  11., 351., 497.,  15.],
                            [138., 199., 206., 300.,  19.],
                            [122., 154., 214., 194.,  18.],
                            [238., 155., 306., 204.,   9.]])


def test_compute_iou():
    result = compute_iou(boxes_A[1, :], boxes_B)
    assert np.allclose(result, target)


def test_compute_ious_shape():
    ious = compute_ious(boxes_A, boxes_B)
    target_shape = (boxes_A.shape[0], boxes_B.shape[0])
    assert ious.shape == target_shape


def test_compute_ious():
    result = compute_ious(boxes_A[1:2, :], boxes_B)
    assert np.allclose(result, target)


def test_denormalize_box():
    box = [.1, .2, .3, .4]
    box = denormalize_box(box, (200, 300))
    assert(box == (30, 40, 90, 80))


def test_to_center_form_inverse():
    assert np.all(to_point_form(to_center_form(boxes_A)) == boxes_A)


def test_to_point_form_inverse():
    assert np.all(to_point_form(to_center_form(boxes_A)) == boxes_A)


def test_to_center_form():
    boxes = to_center_form(boxes_A)
    boxes_A_result = to_point_form(boxes)
    print(boxes_A_result == boxes_A)
    print(boxes)


def test_rotation_matrix_to_quaternion():
    result = rotation_matrix_to_quaternion(affine_matrix[:3, :3])
    assert np.allclose(result, quaternion_target)


def test_rotation_matrix_to_quaternion_inverse():
    quaternion = rotation_matrix_to_quaternion(affine_matrix[:3, :3])
    rotation_matrix = quaternion_to_rotation_matrix(quaternion)
    assert np.allclose(rotation_matrix, affine_matrix[:3, :3])


def test_match_box():
    matched_boxes = match(boxes_with_label, create_prior_boxes('VOC'))
    assert np.array_equal(target_unique_matches,
                          np.unique(matched_boxes[:, :-1], axis=0))


def test_to_encode():
    priors = create_prior_boxes('VOC')
    matches = match(boxes_with_label, priors)
    variances = [.1, .2]
    assert np.all(
        np.round(decode(
            encode(matches, priors, variances), priors, variances)
        ) == matches)


def test_to_decode():
    priors = create_prior_boxes('VOC')
    matches = match(boxes_with_label, priors)
    variances = [.1, .2]
    assert np.all(
        np.round(decode(
            encode(matches, priors, variances), priors, variances)
        ) == matches)


def test_prior_boxes():
    prior_boxes = create_prior_boxes('VOC')
    assert np.all(prior_boxes[:10].astype('float32') == target_prior_boxes)


test_compute_iou()
test_compute_ious()
test_compute_ious_shape()
test_denormalize_box()
test_to_center_form_inverse()
test_to_point_form_inverse()
test_rotation_matrix_to_quaternion()
test_rotation_matrix_to_quaternion_inverse()
test_prior_boxes()
test_match_box()
test_to_encode()
test_to_decode()
